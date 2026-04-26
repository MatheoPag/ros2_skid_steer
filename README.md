# my_robot — Modélisation et simulation (ROS 2 Humble)

Paquet ROS 2 : modèle URDF d’un robot mobile à quatre roues (skid-steer), visualisation **RViz**, simulation **Gazebo Classic** (`gazebo_ros`).

## Prérequis

- **Ubuntu 22.04**, **ROS 2 Humble** — [documentation d’installation](https://docs.ros.org/en/humble/Installation.html)
- Paquets Debian (noms sous Humble) :

```bash
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-plugins \
  ros-humble-teleop-twist-keyboard \
  ros-humble-joint-state-publisher-gui
```

## Mise en place du workspace

Arborescence type :

```text
~/exercice_ros2/
├── src/
│   └── my_robot/
├── build/
├── install/
└── log/
```

Compilation :

```bash
cd ~/exercice_ros2
colcon build --symlink-install
source install/setup.bash
```

Pour les sessions suivantes, sourcer l’environnement depuis la racine du workspace :

```bash
source ~/exercice_ros2/install/setup.bash
```

(Sous **zsh** : `source install/setup.zsh`.)

## Visualisation RViz (sans Gazebo)

Commande :

```bash
ros2 launch my_robot display.launch.py
```

Effet : publication de `/robot_description`, `robot_state_publisher`, états d’articulations, ouverture de **RViz** avec `config/config.rviz`.


| Argument launch | Défaut  | Rôle                                |
| --------------- | ------- | ----------------------------------- |
| `use_sim_time`  | `false` | Horloge simulation (ici désactivée) |
| `rviz`          | `true`  | Affichage RViz                      |
| `gui`           | `true`  | Fenêtre *joint_state_publisher_gui* |


Désactiver RViz : `ros2 launch my_robot display.launch.py rviz:=false`  
Désactiver le GUI des joints : `gui:=false`

Les glisseurs du *joint state publisher GUI* mettent à jour les articulations ; le modèle se met à jour dans RViz.

## Simulation Gazebo et RViz

Commande :

```bash
ros2 launch my_robot launch_sim.launch.py
```

Sans RViz (Gazebo + `robot_state_publisher` + GUI des joints uniquement) :

```bash
ros2 launch my_robot launch_sim.launch.py rviz:=false
```

Effet conjoint :

- nœuds de `display.launch.py` avec `use_sim_time:=true` ;
- **RViz** (`config/config.rviz`) ;
- **Gazebo** via `gazebo_ros` ;
- apparition du robot dans la scène (spawn depuis `/robot_description`).

Monde par défaut : `empty.world` (paquet `gazebo_ros`). Autre monde : `ros2 launch my_robot launch_sim.launch.py world:=/chemin/vers/fichier.world`

La hauteur de spawn (`-z`) est définie dans `launch/launch_sim.launch.py` pour le modèle actuel.

## Contrôle du robot

Dans un second terminal, après `source install/setup.bash` :

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Publication de `geometry_msgs/msg/Twist` sur `**/cmd_vel**`. Le plugin `**gazebo_ros_diff_drive**` (URDF) applique la différentielle sur deux paires de roues (essieux avant et arrière ; gauche / droite couplés).

Consignes exploitées : `linear.x` (marche avant/arrière), `angular.z` (rotation). La composante `linear.y` n’est pas utilisée pour cette cinématique.

## Structure du paquet


| Ressource                    | Emplacement                   |
| ---------------------------- | ----------------------------- |
| Modèle URDF                  | `urdf/robot.urdf`             |
| Launch RViz / état           | `launch/display.launch.py`    |
| Launch Gazebo + RViz + spawn | `launch/launch_sim.launch.py` |
| Configuration RViz           | `config/config.rviz`          |


## Dépannage


| Problème                       | Vérification                                                                                          |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `Package 'my_robot' not found` | `colcon build` puis `source install/setup.bash` depuis le workspace                                   |
| Robot immobile                 | Gazebo et spawn sans erreur ; `ros2 topic echo /cmd_vel` pendant la télécommande                      |
| RViz figé en simulation        | `use_sim_time` à `true` pour les nœuds du launch de simu (déjà paramétré dans `launch_sim.launch.py`) |


