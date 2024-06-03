# Internship

CPU Vs GPU

CPU: Central Processing Unit

Brain of the computer. Fetches, processes and executes commands. Determines how fast programs can run.
CPUs are designed to handle a variety of tasks:
1. including running the operating system
2. executing application programs
3. managing system resources

Features:
1. High Single-Threaded Performance: Complex, more sequencial tasks performed like a thread. Key factors: clock speed, instructions per cycle, efficiency of core (Architectural improvements in the CPU core, such as better branch prediction, larger caches, and more efficient pipelines)
2. Low Latency: delay before a transfer of data begins following an instruction for its transfer. In the context of CPUs, it's the time it takes for the CPU to respond to an instruction and perform a task. Key factors: Cache memory (L1,L2,L3 caches), memory access (fast access times to RAM and efficient memory management), instruction execution (optimized pipelines)

Cores:
CPUs have cores-> fundamental, individual processing units within a CPU, capable of executing its own instructions independently (its like a mini CPU)
Many cores -> Multiple tasks can be performed at once
Each core contains its own set of execution units: ALU, FPU, CU. They also have their own registers small, fast storage locations used to hold data and instructions that are being processed. Cores often have their own dedicated L1 and sometimes L2 cache, which is a small amount of very fast memory used to store frequently accessed data and instructions to speed up processing. It may be shared among multiple cores. Cores typically share a larger L3 cache.
L1 is low capacity but extremely fast, located closest to the core., L2 is slower but has more storage space, and L3 is the slowest of the three but also usually has the biggest storage capacity. L3 cache is shared accross all cores.

CPUs have fewer, more powerful cores optimized for sequential processing, compared to GPU.
CPUs typically have direct access to a smaller, faster cache memory to optimize processing speeds.

Types of memory in CPU:
Register.
RAM stands for random access memory. Any file or application actively in use on a computer is stored in RAM primary memory. 
Cache is a smaller memory configuration reserved from main memory to make computer operations more efficient.
Both RAM and Cache affect latency and clock speeds.


GPU: Graphic Processing Unit

The GPU is specialized hardware designed to accelerate rendering of images, animations, and video for the computer's display. It is also used in scientific computations, machine learning (to train deep neural networks much faster) and data processing (big data analytics, same operations that need to be performed on large datasets multiple times, can happen simultaneously, decreasing process time).
Does parallel processing: how? Using thousands of efficient (but weaker than cpu) cores -> Optimized for handling multiple tasks simultaneously

Uses: Originally designed for rendering graphics, GPUs are now widely used for tasks that benefit from parallel processing, such as scientific computations, machine learning, cryptocurrency mining, and other data-parallel tasks.
Ideal for workloads where the same operation needs to be performed on many pieces of data simultaneously, Thousands of simpler, smaller cores designed for parallel execution.

Cores:
Thousands of smaller simpler cores, fit for parallel processing.

Uses high-bandwidth memory to quickly handle large datasets required for rendering and computation (unlike CPUs which have access to cache memory).
Memory types in GPU:

GPU manufacturers:
1. Nvidia
2. AMD

CUDA is a software from Nvidia that allows you to choose where exactly (memory location) you want to store a particular something in your GPU. It provides full control over you GPU.

GTX and RTX graphic cards (by NVIDIA):
GTX series- aimed at graphics for gaming. Limitations arise in fields of data science and machine learning due to less VRAM.
RTX GPUs often feature more CUDA cores and Tensor cores compared to GTX GPUs. Tensor cores, in particular, are essential for accelerating AI and deep learning tasks. They perform mixed-precision matrix multiplication, significantly speeding up training times for large neural networks.
