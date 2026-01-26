"""
Modern Color Science Module for eSim
References:
- Elliot & Maier (2007): https://doi.org/10.1037/0003-066X.62.4.313
- Singh (2006): https://doi.org/10.1080/0013188042000277323
- Whitfield & Wiltshire (1990): https://doi.org/10.1016/0272-4944(90)90047-3
- Robins & Holmes (2008): https://doi.org/10.1007/s10799-007-0037-4
- Bottomley & Doyle (2006): https://doi.org/10.1002/bdm.515
- W3C WCAG 2.1: https://www.w3.org/TR/WCAG21/
- Rigden (1999): https://doi.org/10.1109/38.768554
"""
import colorsys
from typing import Tuple, List, Dict

class ColorScience:
    # Color psychology mapping (simplified)
    PSYCHOLOGY = {
        'blue':    {'emotion': 'trust', 'hex': '#2563EB'},
        'green':   {'emotion': 'success', 'hex': '#059669'},
        'orange':  {'emotion': 'energy', 'hex': '#D97706'},
        'red':     {'emotion': 'error', 'hex': '#DC2626'},
        'purple':  {'emotion': 'creativity', 'hex': '#7C3AED'},
        'gray':    {'emotion': 'neutral', 'hex': '#64748B'},
    }
    # WCAG 2.1 contrast ratios
    WCAG_AA = 4.5
    WCAG_AAA = 7.0
    # Colorblind simulation matrices (protanopia, deuteranopia, tritanopia)
    COLORBLIND_MATRICES = {
        'protanopia':  (0.56667, 0.43333, 0, 0.55833, 0.44167, 0, 0, 0.24167, 0.75833),
        'deuteranopia':(0.625, 0.375, 0, 0.7, 0.3, 0, 0, 0.3, 0.7),
        'tritanopia':  (0.95, 0.05, 0, 0, 0.43333, 0.56667, 0, 0.475, 0.525),
    }
    # Semantic color system
    SEMANTIC = {
        'primary':   '#2563EB',
        'secondary': '#7C3AED',
        'success':   '#059669',
        'warning':   '#D97706',
        'error':     '#DC2626',
        'info':      '#0891B2',
        'background_light': '#FFFFFF',
        'background_dark':  '#181b24',
        'text_light': '#2c3e50',
        'text_dark':  '#e8eaed',
    }

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hex(r: float, g: float, b: float) -> str:
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    @staticmethod
    def contrast_ratio(hex1: str, hex2: str) -> float:
        def luminance(rgb):
            r, g, b = [x/12.92 if x <= 0.03928 else ((x+0.055)/1.055)**2.4 for x in rgb]
            return 0.2126*r + 0.7152*g + 0.0722*b
        l1 = luminance(ColorScience.hex_to_rgb(hex1))
        l2 = luminance(ColorScience.hex_to_rgb(hex2))
        lighter, darker = max(l1, l2), min(l1, l2)
        return (lighter+0.05)/(darker+0.05)

    @staticmethod
    def ensure_wcag(fg: str, bg: str, level: str = 'AA') -> bool:
        ratio = ColorScience.contrast_ratio(fg, bg)
        return ratio >= (ColorScience.WCAG_AAA if level == 'AAA' else ColorScience.WCAG_AA)

    @staticmethod
    def simulate_colorblind(hex_color: str, mode: str = 'deuteranopia') -> str:
        r, g, b = ColorScience.hex_to_rgb(hex_color)
        m = ColorScience.COLORBLIND_MATRICES.get(mode)
        if not m:
            return hex_color
        r2 = r*m[0] + g*m[1] + b*m[2]
        g2 = r*m[3] + g*m[4] + b*m[5]
        b2 = r*m[6] + g*m[7] + b*m[8]
        return ColorScience.rgb_to_hex(r2, g2, b2)

    @staticmethod
    def harmonious_palette(base: str, mode: str = 'analogous', n: int = 5) -> List[str]:
        # Generate harmonious palette using HSL
        r, g, b = ColorScience.hex_to_rgb(base)
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        palette = []
        if mode == 'analogous':
            for i in range(n):
                h2 = (h + (i - n//2)*0.08) % 1.0
                rgb = colorsys.hls_to_rgb(h2, l, s)
                palette.append(ColorScience.rgb_to_hex(*rgb))
        elif mode == 'complementary':
            palette = [base, ColorScience.rgb_to_hex(*colorsys.hls_to_rgb((h+0.5)%1.0, l, s))]
        elif mode == 'triadic':
            palette = [ColorScience.rgb_to_hex(*colorsys.hls_to_rgb((h+shift)%1.0, l, s)) for shift in (0, 1/3, 2/3)]
        else:
            palette = [base]
        return palette

    @staticmethod
    def adaptive_theme(is_dark: bool) -> Dict[str, str]:
        # Adaptive color scheme
        if is_dark:
            return {
                'background': ColorScience.SEMANTIC['background_dark'],
                'text': ColorScience.SEMANTIC['text_dark'],
                'primary': ColorScience.SEMANTIC['primary'],
                'secondary': ColorScience.SEMANTIC['secondary'],
                'success': ColorScience.SEMANTIC['success'],
                'warning': ColorScience.SEMANTIC['warning'],
                'error': ColorScience.SEMANTIC['error'],
                'info': ColorScience.SEMANTIC['info'],
            }
        else:
            return {
                'background': ColorScience.SEMANTIC['background_light'],
                'text': ColorScience.SEMANTIC['text_light'],
                'primary': ColorScience.SEMANTIC['primary'],
                'secondary': ColorScience.SEMANTIC['secondary'],
                'success': ColorScience.SEMANTIC['success'],
                'warning': ColorScience.SEMANTIC['warning'],
                'error': ColorScience.SEMANTIC['error'],
                'info': ColorScience.SEMANTIC['info'],
            } 