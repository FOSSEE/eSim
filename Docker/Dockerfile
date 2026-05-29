FROM ubuntu:22.04

# Step 1: Install system packages
RUN apt-get update && apt-get install -y \
    lsb-release \
    curl \
    wget \
    sudo \
    unzip \
    python3 \
    python3-venv \
    python3-pip \
    libx11-dev \
    libxcb1 \
    libx11-xcb-dev \
    libxcb-util1 \
    libxcb-xinerama0 \
    libxext6 \
    libxrandr2 \
    libqt5gui5 \
    libqt5core5a \
    libqt5widgets5 \
    libglib2.0-0 \
    libwayland-client0 \
    libwayland-egl1 \
    libxrender1 \
    dbus-x11 \
    mesa-utils \
    software-properties-common \
    xdg-utils \
    evince \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Step 2: Install PyQt5 system-wide (needed for nghdl)
RUN pip3 install --no-cache-dir PyQt5

# Step 3: Create user
RUN useradd -m -s /bin/bash esimuser && \
    echo "esimuser:password" | chpasswd && \
    usermod -aG sudo esimuser && \
    echo "esimuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Step 4: Switch to non-root user
USER esimuser
WORKDIR /home/esimuser

# Step 5: Copy eSim files
COPY --chown=esimuser:esimuser ./esim /home/esimuser/esim/

# Step 6: Make install script executable
RUN chmod +x /home/esimuser/esim/install-eSim.sh

# Step 7: Run install script (non-blocking to avoid Docker build failure)
RUN /home/esimuser/esim/install-eSim.sh --install || echo "eSim install failed. Check logs during runtime."

# Step 8: GUI support
ENV DISPLAY=:0

# Step 9: Default shell
CMD ["bash"]

