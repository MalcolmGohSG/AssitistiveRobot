# Workstation Coach — feasibility brief

An assistive robot for **non-verbal autistic students in a Singapore SPED
school**, coaching activities of daily living (ADL) and vocational / job
skills, noticing when a student needs more support, and staying safe during a
meltdown.

Status: **concept / feasibility**, November 2026. Nothing here is built.
Prices are rough and must be re-checked before purchase. Where a claim comes
from a source it is linked; everything else is the author's engineering
judgement and is marked as an estimate.

> First written in the ToonTheology repo; moved here as the project home.

---

## 1. Recommendation in one paragraph

Build a **tabletop robot fixed to a structured work station**, not a mobile
robot. It shows each step of a task visually, watches the work tray with a
camera, checks each step with deterministic computer vision, and steps its
prompting up or down the way a job coach would. It reads "needs more support"
from **behaviour** (stalls, repeated errors, help button, rising movement or
vocalisation) rather than from facial emotion. During escalation it **never
touches the student**: it goes quiet, stops all demands, and alerts staff.
Print the shell on the Bambu Lab H3C as a rigid frame with a soft TPU skin.
Prove the idea first with a teacher-operated "Wizard-of-Oz" version before
writing any AI.

## 2. Why this shape

| Decision | Reason |
| --- | --- |
| Tabletop, anchored, no wheels | Removes navigation, collision and battery risk, which is most of the safety cost. Coaching happens at a desk anyway. An anchored robot cannot be thrown. |
| Structured work station (TEACCH-style tray with marked zones) | Makes "did the student do step 3?" a solvable vision problem. Open-world action understanding is not reliable enough. |
| Visual-first output | The students are non-verbal; most need visual supports. Short, consistent spoken cues can be paired with visuals, set per student. |
| No speech recognition in v1 | Non-verbal users. Input is big physical buttons and the touchscreen (AAC-style: *help*, *break*, *finished*, *yes/no*). |
| Behaviour signals, not face emotion | Facial-expression models are trained mostly on neurotypical faces and are unreliable for autistic people. Reading emotion from faces is also an ethical problem. Behaviour is observable and checkable by teachers. |
| Robot never physically intervenes | Physical restraint is a trained-staff, protocol-governed act. A machine doing it is unsafe and unacceptable. |

## 3. What the robot does

### 3.1 Skill coaching (ADL and vocational)

Built on established evidence-based practices for autism: **task analysis,
visual supports, video modelling, prompting with a prompt hierarchy, time
delay, and reinforcement**.

- **Teacher authors a task** as a list of steps. Each step has a photo or
  short video (ideally of the student's own teacher or a peer), an expected
  end state on the tray, and a time limit.
- **Per-student prompt ladder**, set by the teacher. For example:
  independent → light cue → picture of step → video model → spoken cue →
  call an adult. Most-to-least or least-to-most is the teacher's choice.
- **Fading**: as a student gets steps right without help, the robot waits
  longer and prompts less. This is the job-coach function: the aim is that
  the student no longer needs the robot.
- **Reinforcement**: the student's own preferred reward (animation, sound,
  token board) after a step or a whole task, as set in their plan.
- **Good first tasks** (to choose with staff): handwashing sequence, folding
  towels or T-shirts, sorting cutlery, packing a lunch box, kit assembly,
  stuffing envelopes or packaging, which are typical SPED vocational bench work.

### 3.2 Checking the student's actions

Deterministic first, AI second:

1. **Overhead camera on the tray**, which has marked zones (AprilTags or
   coloured mats).
2. **Small object detector** trained on the school's *actual* items and run
   on the NPU. Plus **hand tracking** (MediaPipe-class) to know when the
   student is working, idle, or has left.
3. **Step check** = the expected objects are in the expected zone. It's a rule,
   not a guess, so teachers can understand and correct it.
4. A vision-language model is used **only** to help teachers write step
   descriptions and labels, which they then approve. It never decides
   whether a step passed.

### 3.3 "Needs more support": confusion and frustration

The robot does not claim to know what the student feels. It watches for
**support signals** and responds with rules taken from the student's
Behaviour Support Plan:

| Signal | Example response |
| --- | --- |
| No progress past the student's usual time for a step | Next prompt level up |
| Same error twice | Split the step into smaller sub-steps; show video model |
| *Help* button | Show the step again; if pressed again, call an adult |
| *Break* button | Pause the task, show the break visual and a timer |
| Movement or vocal volume rising above the student's own baseline | Drop demands, offer a break or calming item, lower the robot's sound and light |
| Student leaves the station | Pause; tell staff discreetly |

Thresholds are **per student**, learned from a baseline period and adjusted by
teachers. All adjustments are logged so staff can see what the robot did and
why.

**Optional, research only (Phase 3+)**: a wrist biosensor (heart rate, skin
conductance, movement). In inpatient studies of minimally verbal autistic
youth it predicted aggression about 1 minute ahead with about 84% accuracy
(person-specific models) in 2019, and about 3 minutes ahead with about 80%
accuracy in 2024. The researchers say a lot of work remains before it can
be used in homes or schools.
([Northeastern 2019](https://news.northeastern.edu/2019/08/21/this-wearable-device-predicts-aggressive-outbursts-in-people-with-autism-a-minute-in-advance/),
[Northeastern 2024](https://news.northeastern.edu/2024/01/18/autism-aggression-prediction-biosensors/),
[SFARI](https://www.sfari.org/2019/09/30/predicting-aggression-with-wearable-biosensors/)).
Many autistic students won't tolerate a wristband, so this has to stay
optional.

### 3.4 Meltdown: protect the student, protect the robot

**Hard rule: the robot never touches, blocks, follows or restrains a
student.** Staff carry out the school's crisis protocol; the robot supports
them.

| Stage | Robot behaviour |
| --- | --- |
| Early signs (support signals rising) | Stop demands, offer break or calming visual, reduce sound and light. |
| Escalation detected, or staff press a remote button | **Quiet mode**: all motion stops and motors are unpowered, sound off, screen goes dark or shows one calm image. Staff get a discreet alert (pager, watch or tablet). |
| After | Records an antecedent–behaviour–consequence (ABC) entry with timing (no video by default) for the teacher's review of the Behaviour Support Plan. |

**Safety by design**:

- Low-torque, current-limited servos, so a moving part can't hurt a finger.
  Joint gaps are guarded against pinching.
- Rounded shapes. A **soft TPU outer skin** over a rigid frame. No glass:
  the screen sits behind polycarbonate.
- **Clamped or bolted to the table**: it can't be thrown or pulled over. The
  heavy electronics sit in the base.
- No small parts that come off, and tamper-resistant screws (choking
  hazard). Cables run inside the frame, with no loops to grab.
- Mains power through a low-voltage adapter out of reach, so there's no
  battery to be crushed or punctured. If a battery is ever needed, use
  LiFePO4 in a sealed base.
- The **STM32 microcontroller runs a watchdog**: if the Linux side stalls,
  it puts the robot into quiet mode on its own.
- Designed to survive being hit (it's anchored, and the head can give way and
  pop back rather than break).

## 4. Hardware

### 4.1 Robot (per unit, rough estimate in SGD)

| Part | Role | Est. S$ |
| --- | --- | --- |
| Arduino VENTUNO Q (Dragonwing IQ8 + STM32H5, 16 GB) | Vision and coaching logic; MCU for servos, buttons, lights and watchdog. US$399 since 19 Oct 2026 ([CNX](https://www.cnx-software.com/2026/08/25/299-arduino-ventuno-q-sbc-combines-qualcomm-dragonwing-iq8-soc-and-stm32h5-mcu/), [Maketecheasier](https://maketecheasier.com/?p=863180)) | 520 |
| M.2 2230 NVMe, 512 GB–1 TB | Models, task library | 100–150 |
| 10" touchscreen | Visual schedule, step images, video model, AAC buttons | 120–200 |
| 1–2 USB cameras (overhead tray + face-level) | Step checking, presence. A depth camera is **not needed** on a tabletop. | 60–150 |
| Mic array (e.g. ReSpeaker) | Vocalisation *loudness* only, no speech recognition | 80–120 |
| Small speaker | Short cues, reinforcement sounds | 30 |
| 2–3 low-torque smart servos | Expressive head or pointing gesture | 150–250 |
| Large switch-adapted buttons ×3–4 | Help / break / finished / yes-no | 60–150 |
| Light ring, PSU, clamps, cabling | Status and calm lighting, anchoring | 100–150 |
| Filament (frame + TPU skin, incl. iterations) | Enclosure | 100–200 |
| **Total parts per unit** | | **≈ 1,400–2,100** |

Optional: wrist biosensor for research (Phase 3+), at research-grade
device prices.

### 4.2 Bambu Lab H3C, and how to print

- A tool-changer with 9 toolheads: eight for 1.75 mm filament and one for
  2.85 mm TPU (down to 75A), 350 °C hardened nozzles, 65 °C heated chamber.
  The AMS combo is US$2,499 in the US
  ([MatterHackers](https://www.matterhackers.com/store/l/bambu-lab-h3c-tool-changer-3d-printer/),
  [Fauxhammer review](https://www.fauxhammer.com/reviews/bambu-lab-h3c-review-my-best-fdm-printer-yet-but-two-drying-slots/),
  [TechEnclave](https://techenclave.com/news/items/bambu-launches-h3c-3d-printer-with-nine-swappable-print-heads)).
  Build volume was not confirmed in those sources.
- **Why it suits this project**: it can print a rigid frame and a soft TPU
  skin in one job. That makes iteration fast, and each student's unit can be
  customised (low-arousal colours, textured "fidget" panels that come off
  for cleaning but are too large to swallow).
- **Materials**:
  - **PETG or PC** for the frame.
  - **Flame-retardant PC or PETG** around the electronics.
  - **TPU 85A–95A** for the skin and bumpers.
  - **Avoid PLA** for anything that may be hit (it shatters into sharp
    pieces) or that sits near heat.
  - Ask suppliers for REACH/RoHS documents on every filament that touches
    skin.
- **Hygiene**: FDM layer lines trap dirt and saliva, and some students mouth
  objects. Make touch surfaces smooth (TPU, or a sealed coating), and check
  which disinfectant the school uses against each material (alcohol versus
  TPU and PC).
- **Print in a ventilated workshop, not the classroom.** Engineering
  filaments give off particles and fumes while printing.
- Reference standards for the enclosure, even if it isn't legally a toy:
  IEC 62115 (electric toys), EN 71 / ASTM F963 (mechanical and small parts),
  ISO 13482 (personal care robots).

## 5. Software sketch

- **Linux side (Dragonwing)**:
  - Camera pipeline, object detector and hand tracking on the NPU.
  - Coaching engine (a state machine: task → step → prompt level → check →
    reinforce or adjust).
  - Teacher authoring app and a local dashboard.
- **MCU side (STM32H5)**: servos, buttons, lights, quiet mode, watchdog.
- **ROS 2 is not needed** for a robot that doesn't move. A plain service plus
  the board's Linux–MCU bridge is simpler.
- **Teacher tools** (as important as the robot):
  - Build a task from photos and videos.
  - Set each student's prompt ladder, rewards and support-signal rules.
  - See progress: steps done independently, prompt level over time, breaks
    and alerts.
- **Fully offline.** Moxie, an ~US$800 companion robot for children, stopped
  working when its maker closed in December 2024 because it relied on the
  cloud ([Axios](https://www.axios.com/2024/12/10/moxie-kids-robot-shuts-down)).

## 6. Privacy and governance

- Children with disabilities, on camera, in school: **PDPA**, parental
  consent, and school or MOE approval. Get ethics review if a university is
  involved.
- **Process on the device. Don't keep raw video by default.** Store step
  events and counts only. If a teacher wants a clip for review, it is
  opt-in, short-lived and deletable.
- Teachers can see and override everything the robot decides. Each
  student's settings belong to their plan and can be exported or deleted.

## 7. Phased plan (estimate)

| Phase | Duration | Output | Gate to continue |
| --- | --- | --- | --- |
| 0. Co-design | 6–8 wk | With teachers, OT, speech therapist and parents: choose 2–3 tasks and 3–6 students; collect Behaviour Support Plans; ethics and consent; define measures | School commits a class and staff time |
| 1. Wizard-of-Oz | 8–12 wk | Printed shell v1 + screen + buttons; **a teacher triggers prompts from a tablet**. No AI. | Students tolerate it, engage beyond the novelty period, no sensory distress |
| 2. Step checking | 12 wk | Automatic step checks for one task; prompt engine; authoring tool | Step-check accuracy ≥95% on the school's real items |
| 3. Support signals | 12 wk | Per-student support-signal rules, quiet mode, staff alert; optional wristband study | No missed staff alerts in testing; teachers agree with the robot's adjustments |
| 4. Pilot | 8–12 wk | One class, single-case multiple-baseline design (standard in special education research) | Independence improves and staff time is saved |

**Measures**: % of task steps done independently; prompt level over time;
time on task; carry-over to the same task without the robot; staff minutes
per session; number and length of distress episodes; teacher and parent
acceptance.

**People**: roughly 1–2 engineers (embedded/vision + app) for 12–18 months,
plus a part-time special educator or therapist as co-designer. Staff time
will cost more than hardware.

## 8. Market and prior work

| Product | What it is | Takeaway |
| --- | --- | --- |
| QTrobot (LuxAI) | Tabletop social robot for autism therapy; a home RCT with a commercial social robot is running ([arXiv 2604.02642](https://arxiv.org/html/2604.02642v1)) | Social skills focus, not ADL or vocational coaching |
| Milo (RoboKind) | Social-skills robot in 400+ schools; peer-reviewed evidence still limited ([Freethink](https://www.freethink.com/articles/robot-for-autism)) | Sold to schools, which works as a business model |
| Kaspar (U. Hertfordshire) | Long-running research robot for autism | Evidence base, not a product |
| Moxie (Embodied) | Home companion; shut down Dec 2024 ([Axios](https://www.axios.com/2024/12/10/moxie-kids-robot-shuts-down)) | Go offline-first and plan support after sale |
| Obi at CPAS SPED school | Feeding robot for students with multiple disabilities ([NCSS](https://www.ncss.gov.sg/research-and-insights/articles/empowering-independence-with-feeding-robots-at-cerebral-palsy-alliance-singapore--cpas--special-education--school/)) | Singapore SPED schools do adopt assistive robots |
| LOVOT study (AWWA, SUSS, Temasek Foundation) | Social robot in senior care and early intervention centres, Jul 2024 – Mar 2026 ([Temasek Foundation](https://temasekfoundation.org.sg/news/media-releases/first-of-its-kind-singapore-study-shows-ai-social-robots-improve-well-being-across-generations---from-seniors-to-children-with-high-support-needs---and-reduce-caregiver-burden)) | Local partners and funders already exist |

**Gap**: I found no product that combines **skill coaching with step
checking, adaptive prompting, and escalation support** for non-verbal
autistic learners. Existing robots target social skills or companionship.

## 9. Out of scope for v1

Moving around; any physical contact with the student; medication or
safety-critical questions; open-ended chat; facial emotion recognition as a
basis for decisions; cloud dependence.

## 10. Top risks

| Risk | Mitigation |
| --- | --- |
| Engagement fades after the novelty wears off | Phase 1 gate; personal rewards; the robot's role shrinks as the student improves |
| Sensory aversion to the robot | Low-arousal design, adjustable sound and light, co-design with an OT |
| Step-check errors frustrate the student | Fixed tray zones, objects trained per school, teacher override, "unsure → ask adult" |
| A support signal is missed before a meltdown | Robot is an extra layer, never the safety system; staff stay present; remote quiet-mode button |
| Damage during a meltdown | Anchored, soft skin, head that gives way, spare printed parts |
| Privacy breach | On-device only, no raw video kept, consent, deletion |
| Supply (new board, camera makers changing hands) | USB cameras with no lock-in; keep the coaching engine portable to other Linux boards |

## 11. Open questions for the school

1. Which 2–3 tasks matter most for these students' next stage (home, sheltered work, open employment)?
2. How do staff currently prompt and record progress (paper data sheets? an app?)
3. Which students would tolerate a wristband? What is the school's crisis protocol, and who gets alerts?
4. What are the school's rules on cameras in classrooms and on data retention?
5. Is there a university or funder partner (e.g. SUSS, NUS, NTU, SUTD, SG Enable, Temasek Foundation)?
