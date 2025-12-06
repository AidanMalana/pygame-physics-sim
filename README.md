### Install + Run
```sh
git clone https://github.com/AidanMalana/pygame-physics-sim.git
cd pygame-physics-sim

# You probably want to run in a virtual environment:
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python main.py

# Deactivate virtual environment
deactivate
```
### Todo:
- [x] Basic Verlet Integration
- [ ] Rope Sim (Still WIP on my local machine, I showed a half-baked kind of thing in the blog)
- [ ] Procedural Animation
- [ ] Compare Euler vs Verlet
- [ ] Polish

Feel free to make a PR if you want, but be forewarned, I'm probably going to rewrite this whole thing in C over winterbreak for better performance, I just needed to give myself a little python refresher before I take Programming 2
