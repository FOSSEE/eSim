#!/bin/bash
# Prove the freshly built GHDL 4.1.0 (LLVM 18 backend) actually simulates code.
set -uo pipefail
W=/mnt/e/fossee/Evidence_Ubuntu2504/work
mkdir -p "$W/ghdl-test" && cd "$W/ghdl-test"

cat > counter.vhdl <<'VHDL'
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity counter is
    port (clk  : in  std_logic;
          rst  : in  std_logic;
          q    : out unsigned(3 downto 0));
end entity;

architecture rtl of counter is
    signal c : unsigned(3 downto 0) := (others => '0');
begin
    process (clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                c <= (others => '0');
            else
                c <= c + 1;
            end if;
        end if;
    end process;
    q <= c;
end architecture;
VHDL

cat > counter_tb.vhdl <<'VHDL'
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity counter_tb is end entity;

architecture sim of counter_tb is
    signal clk : std_logic := '0';
    signal rst : std_logic := '1';
    signal q   : unsigned(3 downto 0);
begin
    dut : entity work.counter port map (clk => clk, rst => rst, q => q);

    clk <= not clk after 5 ns;

    process
    begin
        wait for 12 ns;
        rst <= '0';
        for i in 1 to 9 loop
            wait until rising_edge(clk);
            report "count = " & integer'image(to_integer(q));
        end loop;
        -- After reset is released on the first sampled edge, eight further
        -- edges have occurred, so the free-running counter reads 8.
        assert to_integer(q) = 8 report "FAILED: expected 8" severity failure;
        report "PASS: counter reached 8 with the LLVM 18 backend";
        std.env.stop;
    end process;
end architecture;
VHDL

echo "=== ghdl --version"
ghdl --version | head -4
echo
echo "=== analysing with the LLVM 18 backend"
ghdl -a --std=08 counter.vhdl counter_tb.vhdl && echo "analyse OK"
echo
echo "=== elaborating"
ghdl -e --std=08 counter_tb && echo "elaborate OK"
echo
echo "=== running the simulation"
ghdl -r --std=08 counter_tb --stop-time=200ns
echo "sim-exit=$?"
