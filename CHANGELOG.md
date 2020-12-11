# # Flappy_Bird_AI CHangelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## 2020-12-10 : Commit : "Optimization. Commenting."
### Changed

1. Finished commenting.
2. More efficient when going through the birds list.
3. Slider to change framerate in real time.
4. I finished all what I planned.

## [Unreleased]

## 2020-12-10 : Commit : "Game in a class. Fixed pipe system."
### Changed

1. Overall structure :
	- Now the game is in a class.
	- A lot of simplifying.
2. Pipes system : 
	- Fixed a bug, when resetting a pipe's position, I had forgotten to call for new random height.
	- Fixed the bug where the space between pipes was not right. Not spacing is a parameter.
3. NeuralNetwork :
	- Calibrating itself using NeuralNetwork.init() after importing the class.

## [Unreleased]

## 2020-12-09 : Commit : "New pipe system. Cleaned Bird Class."
### Changed

1. Pipes system :
	- New optimized pipe system. Only uses 3 pipes.
	- No more bug when a pipe's position overflow.

2. Bird :
	- Bird class is cleaned.
	- Loading Bird image only once.

### To do next
1. Create FlappyBird class, which wille serve as game handler.
2. Remove weights files from GitHub and git ignore pycache.