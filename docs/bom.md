# Hardware, software and price breakdown

November 2026. **Rough estimates for planning, not quotes.** USD prices are
converted at about **US$1 = S$1.30**; Singapore GST (9%) is not included unless
stated. Prices for new robotics parts move quickly: check before buying.
Linked figures are sourced; the rest are the author's estimates.

## Summary

| Bucket | What it buys | Est. S$ |
| --- | --- | --- |
| A. Workshop, one-off | H3C printer, filament stock, tools, training compute | 4,500 – 6,000 |
| B. Track A: workstation coach, per unit | Tabletop coach for SPED classrooms | 1,400 – 2,100 |
| C. Track B: low-cost learning lab | Open-source mobile manipulator for teaching table-setting and tidying by demonstration | 1,500 – 2,800 |
| D. Full-size prototype (concept render), low-cost arms | Mobile base, lift mast, two light arms, head, guide handle | 6,500 – 10,500 |
| D′. Same, with capable arms | Arms strong enough for a pot, kettle or full bowl | 20,000 – 40,000+ |
| E. Software | Almost all free and open source | 0 – 1,000 / yr |
| F. Contingency | Breakage, redesign, shipping | +25% of hardware |

**A sensible first-year spend is about S$9,000–13,000** (A + B + C + one D
prototype with low-cost arms). People's time costs much more than this.

Commercial comparison: Hello Robot Stretch is about US$25–30k
([Robot Report](https://www.therobotreport.com/stretch-3-mobile-manipulator-hello-robot-designed-open-source-development/),
[IEEE Spectrum](https://spectrum.ieee.org/stretch-4-home-robot)). 1X NEO is US$20k
or US$499/month, relying on remote human operators at first
([eWeek](https://www.eweek.com/news/1x-neo-humanoid-home-robot-2026/)).

## A. Workshop (one-off)

| Item | Notes | Est. S$ |
| --- | --- | --- |
| Bambu Lab H3C AMS Combo | US$2,499 ([MatterHackers](https://www.matterhackers.com/store/l/bambu-lab-h3c-tool-changer-3d-printer/)); SG price incl. GST will differ | 3,300 – 3,600 |
| Filament stock | PETG, PC / PC-FR, TPU 85–95A, PLA for quick fit tests | 300 – 500 |
| Tools | Soldering station, multimeter, crimpers, bench power supply, hex and Torx drivers, calipers | 300 – 600 |
| Training compute, **rent first** | RTX 5090 cloud rental from about US$0.50/hr; H100 about US$1.4–4.3/hr ([AMCompute](https://www.amcompute.com/gpu-cloud-prices/rtx-5090), [Tech Insider](https://tech-insider.org/what-renting-an-nvidia-h100-costs-per-hour-in-2026-and-when-renting-beats-buying/)). A few hundred hours a year for imitation learning | 300 – 1,000 / yr |
| Optional: own GPU PC | RTX 5090 was about S$4,947 for the card alone in July 2026 ([GPUPrix](https://gpuprix.com/de/singapore/gpus/geforce-rtx-5090)); a whole PC costs about S$7–9k. Only worth it once you're training every week | (7,000 – 9,000) |

You already have a computer for development; it doesn't need a GPU, because training runs on rented machines.

## B. Track A: workstation coach (per unit)

See [feasibility.md](feasibility.md) §4.1. VENTUNO Q (US$399), NVMe, 10″
touchscreen, 1–2 USB cameras, mic array, speaker, 2–3 low-torque servos,
switch-adapted buttons, light ring, power, clamps, filament.
**About S$1,400–2,100.**

## C. Track B: low-cost learning lab

| Item | Notes | Est. S$ |
| --- | --- | --- |
| XLeRobot build | Two arms on a mobile base: about US$660 in parts; about US$1,300 with onboard compute ([docs](https://xlerobot.readthedocs.io/en/latest/), [arXiv](https://arxiv.org/pdf/2603.09051)) | 900 – 1,700 |
| SO-101 leader arms for teleoperation | You demonstrate a task with the leader arms and the robot learns from it; about US$230 per leader+follower pair DIY ([roboticscenter.ai](https://roboticscenter.ai/hardware/so-101)) | 300 – 600 |
| Extra cameras, mats, practice items | Bowls, chopsticks, cups, tray | 150 – 300 |
| Printed parts | Printed on the H3C | 100 – 200 |

## D. Full-size prototype (the concept render)

| Subsystem | Parts | Est. S$ |
| --- | --- | --- |
| Compute | Arduino VENTUNO Q, US$399 ([CNX](https://www.cnx-software.com/2026/08/25/299-arduino-ventuno-q-sbc-combines-qualcomm-dragonwing-iq8-soc-and-stm32h5-mcu/)) + 1 TB NVMe | 640 – 700 |
| Drive base | 2 brushless hub motors, CAN-capable FOC drivers (ODrive or moteus class), casters, aluminium frame | 1,100 – 2,000 |
| Power | 24 V LiFePO4 about 20 Ah with BMS, charger, DC-DC converters, fuses | 500 – 850 |
| Lift mast | Lead-screw or belt lift that holds position with power off, 40–60 cm travel (floor to counter height) | 300 – 800 |
| Arms, low-cost | 2 × SO-101 class (payload of a few hundred grams: chopsticks, bowls, cups; **not** a pot of water) + leader arms for teaching | 600 – 900 |
| Navigation sensors | RPLIDAR C1, about US$80–100 ([Waveshare](https://www.waveshare.com/rplidar-c1.htm)); 2 depth cameras (head + low front, RealSense or Orbbec class); 2 wrist cameras; IMU | 900 – 1,500 |
| Stair and edge safety | Downward ToF or cliff sensors, bumper switches inside the TPU ring | 100 – 200 |
| Interaction | 10″ screen, AAC buttons, mic array, speaker, light ring | 350 – 500 |
| Safety chain | Mushroom e-stop, safety relay or contactor that cuts motor power in hardware | 150 – 300 |
| Guide handle | Rigid handle with load cell (senses how hard the person pulls) and vibration motor | 100 – 200 |
| Enclosure | PETG / PC-FR frame panels, TPU skin and bumpers | 300 – 600 |
| Wiring and fasteners | Connectors, cable chain, tamper-resistant screws | 200 – 300 |
| **Total (low-cost arms)** | | **≈ 5,250 – 8,850**, about 6,500–10,500 with 25% contingency |

**About D′ (capable arms).** Boiling an egg, making noodles and setting a full
table need arms that can lift about 1–3 kg safely. Small collaborative arms
cost several thousand to over S$15k each, which is how the total reaches
S$20–40k+. Keep the hot work to appliances (egg cooker, hot-water dispenser)
and the light-arm version can still do a useful subset.

**Not in v1 at any price: carrying or supporting a person on stairs.** The
robot can guide someone to the stairs, announce them, and help them find the
handrail.

## E. Software

| Layer | Choice | Cost |
| --- | --- | --- |
| OS and middleware | Ubuntu, ROS 2 Jazzy, Nav2 (navigation), MoveIt 2 (arm motion), ros2_control | Free |
| Board tools | Arduino App Lab / `arduino-cli`, RouterBridge ROS library | Free |
| Learning from demonstration | Hugging Face LeRobot (ACT, diffusion policy, SmolVLA, pi0-class models) | Free |
| Simulation | MuJoCo, Gazebo, Isaac Sim | Free |
| On-robot models | llama.cpp or Qualcomm AI Hub models, Whisper, Piper TTS, small vision-language model | Free (check each model's licence) |
| CAD and printing | build123d / CadQuery (precise parts), Blender (shell and renders), Bambu Studio | Free |
| Coding assistant | Claude: the subscription you already have; API usage for off-robot authoring tools | Existing + about S$10–50 / month |
| Project site | GitHub (code, Issues, Discussions) + Cloudflare Pages for `lab.toontheology.com` | Free tier |

## Not costed here

- Engineering and specialist time. This is the largest cost by far.
- Safety assessment against ISO 13482 by a test lab before any use with students. Ask a lab for a quote.
- Ethics review, insurance, and PDPA work for the school pilot.
