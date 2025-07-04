#  eSim Docker Image

This branch provides a Docker-based environment for running **eSim 2.5** in a portable and pre-configured container. It eliminates system-specific installation issues and provides a plug-and-play experience across supported Linux distributions.

---

## 🐳 What This Docker Image Includes

- **Ubuntu 22.04** base system
    
- Pre-installed **eSim 2.5**
    
- All required dependencies and libraries (Qt, Python, Verilator, GHDL, etc.)
    
- **PyQt5** (via pip) for NGHDL support
    
- **PDF viewer (**`evince`**)** to view the user manual inside the container
    
- **Non-root user** (`esimuser`) for safer execution
    
- **GUI support** via host X11 socket
    
- **No installation prompts** — fully automated setup during build
    

---

## 🚧 Prerequisites

- Docker installed on the host machine
    
- X11 support enabled on the host (for GUI apps)
    
- Linux host (tested on Ubuntu 22.04+, may work on others)
    

---

##  Building the Image

1. Download the eSim Ubuntu 2.5 installer (.zip) and extract it and rename as esim/

2. Modify the relevant installer script inside the folder install-eSim-scripts/ with the following changes:
   > add "cd esim/" at the start
   
   > update the function copyKicadLibrary with the following code:
   
   
            function copyKicadLibrary {
                echo "Setting up KiCad libraries for eSim..."
            
                if [[ ! -d library/kicadLibrary ]]; then
                    echo "Error: 'library/kicadLibrary' folder not found!"
                    exit 1
                fi
            
                # Ensure user config directory exists
                mkdir -p ~/.config/kicad/6.0
            
                # Copy custom symbol table
                cp library/kicadLibrary/template/sym-lib-table ~/.config/kicad/6.0/
                echo "Symbol table copied to ~/.config/kicad/6.0/"
            
                # Copy custom symbols
                sudo cp -r library/kicadLibrary/eSim-symbols/* /usr/share/kicad/symbols/
                echo "Custom symbols copied to /usr/share/kicad/symbols/"
            
                # Fix ownership if needed
                sudo chown -R "$USER:$USER" /usr/share/kicad/symbols/
            
                echo "KiCad library setup complete."
            }
        
        
   > Comment all lines from "Enter proxy details if you are connected to internet thorugh proxy" until the comment "# Calling functions"
   
   > Comment all lines below the comment "# Generating esim.desktop file" under the function createDesktopStartScript
   
   > extract kicadLibrary into the library as library/kicadLibrary/

3. Place the Dockerfile in the same directory as the esim/ folder

4. Open the terminal at the location of the Dockerfile and RUN the command:

    ```
    docker build -t esim-2.5 .
    ```

This will create a Docker image named `esim-2.5` with eSim fully installed and ready to run.

---

## ▶️ Running the Container

Before launching, allow Docker access to your X server:

```
xhost +local:docker
```

Then run the container:

```
docker run -it \
  --env DISPLAY=$DISPLAY \
  --volume /tmp/.X11-unix:/tmp/.X11-unix \
  esim-2.5
```

Once inside the container, launch eSim with:

```
esim
```

---

## 🧠 Notes

- This image does **not include persistent storage** by default. Files created inside the container will be lost once it is stopped.
    
- Future updates may support **volume mounting** for project persistence.
    
- The **DevDocs browser shortcut is disabled** inside the Docker version (no browser is installed). A link is printed in the terminal for reference.
    

---

## 📌 Future Improvements

- Add **shared volume support** to save project files outside the container
    
- Serve documentation through a **lightweight internal web server**
    
- **Push prebuilt image to DockerHub**
    
- Add support for additional **Linux distros** and **ARM-based systems**
    

---
