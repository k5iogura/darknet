![Darknet Logo](http://pjreddie.com/media/files/darknet-black-small.png)
<img src="https://github.com/k5iogura/darknet_ttt/files/Magic_formation.jpg" alt="logo" width="250"/>

# Darknet
**Darknet** is an open source neural network framework written in C and CUDA. It is fast, easy to install, and supports CPU and GPU computation.

***

### What's darknet_sdl  

darknet GUI is custom program or OpenCV+LibGtk+ libraries.  
We try to implement darknet on ARM Cortex-A9 Proccessor, also try to accellaration by Altera SoC-FPGA.  We were hard to implement OpenCV+LibGtk+ onto ARM linux.  We decided **to use SDL instead of LibGtk+** as GUI of darknet.  

darknet **_sdl** means darknet+SDL.  SDL is powerfull and simple library to create X11 Client program.  And SDL is programmed by *Pure C Language*, so, it's so easy to implement onto ARM Linux.  

We make wrapper of OpenCV by SDL APIs.  

***

For more information see the [Darknet project website](http://pjreddie.com/darknet).

For questions or issues please use the [Google Group](https://groups.google.com/forum/#!forum/darknet).
