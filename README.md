# Genetic-Algorithm-Smart-Rockets

Simple genetic algorithm based on the Smart Rockets by blprnt. It follows the next rules:
-Each rocket has the upper circle as a target.
-Each rocket has an array of vectors that determine its movements. This vectors are initialized randomly.
-Every x frames, the generation dies and a new one borns.
-Every new rocket has the DNA (Movement Vectors), of a "randomly" choosen parents os the last generation.
-The DNA of a rocket its more likely to be chosen in the next generation if they get closer to the target.
-The maximum score is got when a rocket touches the target.
-The minimum score is got when a rocket touches the game boundaries (dies).
