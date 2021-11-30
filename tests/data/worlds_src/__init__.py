# bedrock worlds
bedrock_vanilla_1_16 = "bedrock_vanilla_1_16"

BedrockLevels = [bedrock_vanilla_1_16]

# java worlds
java_vanilla_1_13 = "java_vanilla_1_13"
java_vanilla_1_12_2 = "java_vanilla_1_12_2"
java_vanilla_1_16_5_dimension = "java_vanilla_1_16_5_dimension"

JavaVanillaLevels = [
    java_vanilla_1_13,
    java_vanilla_1_12_2,
    java_vanilla_1_16_5_dimension,
]

# java forge worlds
java_forge_1_12_2_twilight_forest = "java_forge_1_12_2_twilight_forest"
java_forge_1_16_5_twilight_forest = "java_forge_1_16_5_twilight_forest"

JavaModdedLevels = [
    java_forge_1_12_2_twilight_forest,
    java_forge_1_16_5_twilight_forest,
]

JavaLevels = [*JavaVanillaLevels, *JavaModdedLevels]

levels = [
    *BedrockLevels,
    *JavaLevels,
]