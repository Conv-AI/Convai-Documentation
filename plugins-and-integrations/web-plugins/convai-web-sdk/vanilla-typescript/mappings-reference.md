---
title: Blendshape channel order reference
description: Reference for the channel order of the ARKit and MetaHuman blendshape frames that the Convai Web SDK streams for lip sync and facial animation.
last_reviewed: "1.9.4"
---

Each blendshape frame in `client.blendshapeQueue` is a `Float32Array` whose position `i` holds the value of channel `i` below. The order depends on `blendshapeConfig.format` and applies to raw frames, before any `customMapper` changes them. Both tables are exported from `@convai/web-sdk/lipsync-helpers`, so read them in code instead of copying them.

## ARKit order

`ARKIT_ORDER_61` gives the order of `format: "arkit"` frames: 61 values. Indexes 0 to 51 are the 52 ARKit facial blendshapes, in an order that differs from Apple's standard order. Indexes 52 to 60 are head and eye rotations.

| Index | Channel |
|---|---|
| 0 | `EyeBlinkLeft` |
| 1 | `EyeLookDownLeft` |
| 2 | `EyeLookInLeft` |
| 3 | `EyeLookOutLeft` |
| 4 | `EyeLookUpLeft` |
| 5 | `EyeSquintLeft` |
| 6 | `EyeWideLeft` |
| 7 | `EyeBlinkRight` |
| 8 | `EyeLookDownRight` |
| 9 | `EyeLookInRight` |
| 10 | `EyeLookOutRight` |
| 11 | `EyeLookUpRight` |
| 12 | `EyeSquintRight` |
| 13 | `EyeWideRight` |
| 14 | `JawForward` |
| 15 | `JawRight` |
| 16 | `JawLeft` |
| 17 | `JawOpen` |
| 18 | `MouthClose` |
| 19 | `MouthFunnel` |
| 20 | `MouthPucker` |
| 21 | `MouthRight` |
| 22 | `MouthLeft` |
| 23 | `MouthSmileLeft` |
| 24 | `MouthSmileRight` |
| 25 | `MouthFrownLeft` |
| 26 | `MouthFrownRight` |
| 27 | `MouthDimpleLeft` |
| 28 | `MouthDimpleRight` |
| 29 | `MouthStretchLeft` |
| 30 | `MouthStretchRight` |
| 31 | `MouthRollLower` |
| 32 | `MouthRollUpper` |
| 33 | `MouthShrugLower` |
| 34 | `MouthShrugUpper` |
| 35 | `MouthPressLeft` |
| 36 | `MouthPressRight` |
| 37 | `MouthLowerDownLeft` |
| 38 | `MouthLowerDownRight` |
| 39 | `MouthUpperUpLeft` |
| 40 | `MouthUpperUpRight` |
| 41 | `BrowDownLeft` |
| 42 | `BrowDownRight` |
| 43 | `BrowInnerUp` |
| 44 | `BrowOuterUpLeft` |
| 45 | `BrowOuterUpRight` |
| 46 | `CheekPuff` |
| 47 | `CheekSquintLeft` |
| 48 | `CheekSquintRight` |
| 49 | `NoseSneerLeft` |
| 50 | `NoseSneerRight` |
| 51 | `TongueOut` |
| 52 | `HeadYaw` |
| 53 | `HeadPitch` |
| 54 | `HeadRoll` |
| 55 | `LeftEyeYaw` |
| 56 | `LeftEyePitch` |
| 57 | `LeftEyeRoll` |
| 58 | `RightEyeYaw` |
| 59 | `RightEyePitch` |
| 60 | `RightEyeRoll` |

`STANDARD_ARKIT_ORDER` holds the 52 facial blendshapes in Apple's standard order, and `convertOrder61ToStandard(values61)` reorders a 61-value frame into it. `mapOrder61ToNames(values61)` returns the frame as an object keyed by channel name. `getHeadRotation`, `getEyeRotations`, and `getLipSyncValuesFromOrder61` read subsets of a frame.

## MetaHuman order

`METAHUMAN_ORDER_251` gives the order of `format: "mha"` frames: 251 values, each named after a MetaHuman `CTRL_expressions_` control.

| Index | Channel |
|---|---|
| 0 | `CTRL_expressions_browDownL` |
| 1 | `CTRL_expressions_browDownR` |
| 2 | `CTRL_expressions_browLateralL` |
| 3 | `CTRL_expressions_browLateralR` |
| 4 | `CTRL_expressions_browRaiseInL` |
| 5 | `CTRL_expressions_browRaiseInR` |
| 6 | `CTRL_expressions_browRaiseOuterL` |
| 7 | `CTRL_expressions_browRaiseOuterR` |
| 8 | `CTRL_expressions_earUpL` |
| 9 | `CTRL_expressions_earUpR` |
| 10 | `CTRL_expressions_eyeBlinkL` |
| 11 | `CTRL_expressions_eyeBlinkR` |
| 12 | `CTRL_expressions_eyeCheekRaiseL` |
| 13 | `CTRL_expressions_eyeCheekRaiseR` |
| 14 | `CTRL_expressions_eyeFaceScrunchL` |
| 15 | `CTRL_expressions_eyeFaceScrunchR` |
| 16 | `CTRL_expressions_eyeLidPressL` |
| 17 | `CTRL_expressions_eyeLidPressR` |
| 18 | `CTRL_expressions_eyeLookDownL` |
| 19 | `CTRL_expressions_eyeLookDownR` |
| 20 | `CTRL_expressions_eyeLookLeftL` |
| 21 | `CTRL_expressions_eyeLookLeftR` |
| 22 | `CTRL_expressions_eyeLookRightL` |
| 23 | `CTRL_expressions_eyeLookRightR` |
| 24 | `CTRL_expressions_eyeLookUpL` |
| 25 | `CTRL_expressions_eyeLookUpR` |
| 26 | `CTRL_expressions_eyeLowerLidDownL` |
| 27 | `CTRL_expressions_eyeLowerLidDownR` |
| 28 | `CTRL_expressions_eyeLowerLidUpL` |
| 29 | `CTRL_expressions_eyeLowerLidUpR` |
| 30 | `CTRL_expressions_eyeParallelLookDirection` |
| 31 | `CTRL_expressions_eyePupilNarrowL` |
| 32 | `CTRL_expressions_eyePupilNarrowR` |
| 33 | `CTRL_expressions_eyePupilWideL` |
| 34 | `CTRL_expressions_eyePupilWideR` |
| 35 | `CTRL_expressions_eyeRelaxL` |
| 36 | `CTRL_expressions_eyeRelaxR` |
| 37 | `CTRL_expressions_eyeSquintInnerL` |
| 38 | `CTRL_expressions_eyeSquintInnerR` |
| 39 | `CTRL_expressions_eyeUpperLidUpL` |
| 40 | `CTRL_expressions_eyeUpperLidUpR` |
| 41 | `CTRL_expressions_eyeWidenL` |
| 42 | `CTRL_expressions_eyeWidenR` |
| 43 | `CTRL_expressions_eyelashesDownINL` |
| 44 | `CTRL_expressions_eyelashesDownINR` |
| 45 | `CTRL_expressions_eyelashesDownOUTL` |
| 46 | `CTRL_expressions_eyelashesDownOUTR` |
| 47 | `CTRL_expressions_eyelashesUpINL` |
| 48 | `CTRL_expressions_eyelashesUpINR` |
| 49 | `CTRL_expressions_eyelashesUpOUTL` |
| 50 | `CTRL_expressions_eyelashesUpOUTR` |
| 51 | `CTRL_expressions_jawBack` |
| 52 | `CTRL_expressions_jawChinCompressL` |
| 53 | `CTRL_expressions_jawChinCompressR` |
| 54 | `CTRL_expressions_jawChinRaiseDL` |
| 55 | `CTRL_expressions_jawChinRaiseDR` |
| 56 | `CTRL_expressions_jawChinRaiseUL` |
| 57 | `CTRL_expressions_jawChinRaiseUR` |
| 58 | `CTRL_expressions_jawClenchL` |
| 59 | `CTRL_expressions_jawClenchR` |
| 60 | `CTRL_expressions_jawFwd` |
| 61 | `CTRL_expressions_jawLeft` |
| 62 | `CTRL_expressions_jawOpen` |
| 63 | `CTRL_expressions_jawOpenExtreme` |
| 64 | `CTRL_expressions_jawRight` |
| 65 | `CTRL_expressions_mouthCheekBlowL` |
| 66 | `CTRL_expressions_mouthCheekBlowR` |
| 67 | `CTRL_expressions_mouthCheekSuckL` |
| 68 | `CTRL_expressions_mouthCheekSuckR` |
| 69 | `CTRL_expressions_mouthCornerDepressL` |
| 70 | `CTRL_expressions_mouthCornerDepressR` |
| 71 | `CTRL_expressions_mouthCornerDownL` |
| 72 | `CTRL_expressions_mouthCornerDownR` |
| 73 | `CTRL_expressions_mouthCornerNarrowL` |
| 74 | `CTRL_expressions_mouthCornerNarrowR` |
| 75 | `CTRL_expressions_mouthCornerPullL` |
| 76 | `CTRL_expressions_mouthCornerPullR` |
| 77 | `CTRL_expressions_mouthCornerRounderDL` |
| 78 | `CTRL_expressions_mouthCornerRounderDR` |
| 79 | `CTRL_expressions_mouthCornerRounderUL` |
| 80 | `CTRL_expressions_mouthCornerRounderUR` |
| 81 | `CTRL_expressions_mouthCornerSharpenDL` |
| 82 | `CTRL_expressions_mouthCornerSharpenDR` |
| 83 | `CTRL_expressions_mouthCornerSharpenUL` |
| 84 | `CTRL_expressions_mouthCornerSharpenUR` |
| 85 | `CTRL_expressions_mouthCornerUpL` |
| 86 | `CTRL_expressions_mouthCornerUpR` |
| 87 | `CTRL_expressions_mouthCornerWideL` |
| 88 | `CTRL_expressions_mouthCornerWideR` |
| 89 | `CTRL_expressions_mouthDimpleL` |
| 90 | `CTRL_expressions_mouthDimpleR` |
| 91 | `CTRL_expressions_mouthDown` |
| 92 | `CTRL_expressions_mouthFunnelDL` |
| 93 | `CTRL_expressions_mouthFunnelDR` |
| 94 | `CTRL_expressions_mouthFunnelUL` |
| 95 | `CTRL_expressions_mouthFunnelUR` |
| 96 | `CTRL_expressions_mouthLeft` |
| 97 | `CTRL_expressions_mouthLipsBlowL` |
| 98 | `CTRL_expressions_mouthLipsBlowR` |
| 99 | `CTRL_expressions_mouthLipsPressL` |
| 100 | `CTRL_expressions_mouthLipsPressR` |
| 101 | `CTRL_expressions_mouthLipsPullDL` |
| 102 | `CTRL_expressions_mouthLipsPullDR` |
| 103 | `CTRL_expressions_mouthLipsPullUL` |
| 104 | `CTRL_expressions_mouthLipsPullUR` |
| 105 | `CTRL_expressions_mouthLipsPurseDL` |
| 106 | `CTRL_expressions_mouthLipsPurseDR` |
| 107 | `CTRL_expressions_mouthLipsPurseUL` |
| 108 | `CTRL_expressions_mouthLipsPurseUR` |
| 109 | `CTRL_expressions_mouthLipsPushDL` |
| 110 | `CTRL_expressions_mouthLipsPushDR` |
| 111 | `CTRL_expressions_mouthLipsPushUL` |
| 112 | `CTRL_expressions_mouthLipsPushUR` |
| 113 | `CTRL_expressions_mouthLipsStickyLPh1` |
| 114 | `CTRL_expressions_mouthLipsStickyLPh2` |
| 115 | `CTRL_expressions_mouthLipsStickyLPh3` |
| 116 | `CTRL_expressions_mouthLipsStickyRPh1` |
| 117 | `CTRL_expressions_mouthLipsStickyRPh2` |
| 118 | `CTRL_expressions_mouthLipsStickyRPh3` |
| 119 | `CTRL_expressions_mouthLipsThickDL` |
| 120 | `CTRL_expressions_mouthLipsThickDR` |
| 121 | `CTRL_expressions_mouthLipsThickInwardDL` |
| 122 | `CTRL_expressions_mouthLipsThickInwardDR` |
| 123 | `CTRL_expressions_mouthLipsThickInwardUL` |
| 124 | `CTRL_expressions_mouthLipsThickInwardUR` |
| 125 | `CTRL_expressions_mouthLipsThickUL` |
| 126 | `CTRL_expressions_mouthLipsThickUR` |
| 127 | `CTRL_expressions_mouthLipsThinDL` |
| 128 | `CTRL_expressions_mouthLipsThinDR` |
| 129 | `CTRL_expressions_mouthLipsThinInwardDL` |
| 130 | `CTRL_expressions_mouthLipsThinInwardDR` |
| 131 | `CTRL_expressions_mouthLipsThinInwardUL` |
| 132 | `CTRL_expressions_mouthLipsThinInwardUR` |
| 133 | `CTRL_expressions_mouthLipsThinUL` |
| 134 | `CTRL_expressions_mouthLipsThinUR` |
| 135 | `CTRL_expressions_mouthLipsTightenDL` |
| 136 | `CTRL_expressions_mouthLipsTightenDR` |
| 137 | `CTRL_expressions_mouthLipsTightenUL` |
| 138 | `CTRL_expressions_mouthLipsTightenUR` |
| 139 | `CTRL_expressions_mouthLipsTogetherDL` |
| 140 | `CTRL_expressions_mouthLipsTogetherDR` |
| 141 | `CTRL_expressions_mouthLipsTogetherUL` |
| 142 | `CTRL_expressions_mouthLipsTogetherUR` |
| 143 | `CTRL_expressions_mouthLipsTowardsDL` |
| 144 | `CTRL_expressions_mouthLipsTowardsDR` |
| 145 | `CTRL_expressions_mouthLipsTowardsUL` |
| 146 | `CTRL_expressions_mouthLipsTowardsUR` |
| 147 | `CTRL_expressions_mouthLowerLipBiteL` |
| 148 | `CTRL_expressions_mouthLowerLipBiteR` |
| 149 | `CTRL_expressions_mouthLowerLipDepressL` |
| 150 | `CTRL_expressions_mouthLowerLipDepressR` |
| 151 | `CTRL_expressions_mouthLowerLipRollInL` |
| 152 | `CTRL_expressions_mouthLowerLipRollInR` |
| 153 | `CTRL_expressions_mouthLowerLipRollOutL` |
| 154 | `CTRL_expressions_mouthLowerLipRollOutR` |
| 155 | `CTRL_expressions_mouthLowerLipShiftLeft` |
| 156 | `CTRL_expressions_mouthLowerLipShiftRight` |
| 157 | `CTRL_expressions_mouthLowerLipTowardsTeethL` |
| 158 | `CTRL_expressions_mouthLowerLipTowardsTeethR` |
| 159 | `CTRL_expressions_mouthPressDL` |
| 160 | `CTRL_expressions_mouthPressDR` |
| 161 | `CTRL_expressions_mouthPressUL` |
| 162 | `CTRL_expressions_mouthPressUR` |
| 163 | `CTRL_expressions_mouthRight` |
| 164 | `CTRL_expressions_mouthSharpCornerPullL` |
| 165 | `CTRL_expressions_mouthSharpCornerPullR` |
| 166 | `CTRL_expressions_mouthStickyDC` |
| 167 | `CTRL_expressions_mouthStickyDINL` |
| 168 | `CTRL_expressions_mouthStickyDINR` |
| 169 | `CTRL_expressions_mouthStickyDOUTL` |
| 170 | `CTRL_expressions_mouthStickyDOUTR` |
| 171 | `CTRL_expressions_mouthStickyUC` |
| 172 | `CTRL_expressions_mouthStickyUINL` |
| 173 | `CTRL_expressions_mouthStickyUINR` |
| 174 | `CTRL_expressions_mouthStickyUOUTL` |
| 175 | `CTRL_expressions_mouthStickyUOUTR` |
| 176 | `CTRL_expressions_mouthStretchL` |
| 177 | `CTRL_expressions_mouthStretchLipsCloseL` |
| 178 | `CTRL_expressions_mouthStretchLipsCloseR` |
| 179 | `CTRL_expressions_mouthStretchR` |
| 180 | `CTRL_expressions_mouthUp` |
| 181 | `CTRL_expressions_mouthUpperLipBiteL` |
| 182 | `CTRL_expressions_mouthUpperLipBiteR` |
| 183 | `CTRL_expressions_mouthUpperLipRaiseL` |
| 184 | `CTRL_expressions_mouthUpperLipRaiseR` |
| 185 | `CTRL_expressions_mouthUpperLipRollInL` |
| 186 | `CTRL_expressions_mouthUpperLipRollInR` |
| 187 | `CTRL_expressions_mouthUpperLipRollOutL` |
| 188 | `CTRL_expressions_mouthUpperLipRollOutR` |
| 189 | `CTRL_expressions_mouthUpperLipShiftLeft` |
| 190 | `CTRL_expressions_mouthUpperLipShiftRight` |
| 191 | `CTRL_expressions_mouthUpperLipTowardsTeethL` |
| 192 | `CTRL_expressions_mouthUpperLipTowardsTeethR` |
| 193 | `CTRL_expressions_neckDigastricDown` |
| 194 | `CTRL_expressions_neckDigastricUp` |
| 195 | `CTRL_expressions_neckMastoidContractL` |
| 196 | `CTRL_expressions_neckMastoidContractR` |
| 197 | `CTRL_expressions_neckStretchL` |
| 198 | `CTRL_expressions_neckStretchR` |
| 199 | `CTRL_expressions_neckSwallowPh1` |
| 200 | `CTRL_expressions_neckSwallowPh2` |
| 201 | `CTRL_expressions_neckSwallowPh3` |
| 202 | `CTRL_expressions_neckSwallowPh4` |
| 203 | `CTRL_expressions_neckThroatDown` |
| 204 | `CTRL_expressions_neckThroatExhale` |
| 205 | `CTRL_expressions_neckThroatInhale` |
| 206 | `CTRL_expressions_neckThroatUp` |
| 207 | `CTRL_expressions_noseNasolabialDeepenL` |
| 208 | `CTRL_expressions_noseNasolabialDeepenR` |
| 209 | `CTRL_expressions_noseNostrilCompressL` |
| 210 | `CTRL_expressions_noseNostrilCompressR` |
| 211 | `CTRL_expressions_noseNostrilDepressL` |
| 212 | `CTRL_expressions_noseNostrilDepressR` |
| 213 | `CTRL_expressions_noseNostrilDilateL` |
| 214 | `CTRL_expressions_noseNostrilDilateR` |
| 215 | `CTRL_expressions_noseWrinkleL` |
| 216 | `CTRL_expressions_noseWrinkleR` |
| 217 | `CTRL_expressions_noseWrinkleUpperL` |
| 218 | `CTRL_expressions_noseWrinkleUpperR` |
| 219 | `CTRL_expressions_teethBackD` |
| 220 | `CTRL_expressions_teethBackU` |
| 221 | `CTRL_expressions_teethDownD` |
| 222 | `CTRL_expressions_teethDownU` |
| 223 | `CTRL_expressions_teethFwdD` |
| 224 | `CTRL_expressions_teethFwdU` |
| 225 | `CTRL_expressions_teethLeftD` |
| 226 | `CTRL_expressions_teethLeftU` |
| 227 | `CTRL_expressions_teethRightD` |
| 228 | `CTRL_expressions_teethRightU` |
| 229 | `CTRL_expressions_teethUpD` |
| 230 | `CTRL_expressions_teethUpU` |
| 231 | `CTRL_expressions_tongueBendDown` |
| 232 | `CTRL_expressions_tongueBendUp` |
| 233 | `CTRL_expressions_tongueDown` |
| 234 | `CTRL_expressions_tongueIn` |
| 235 | `CTRL_expressions_tongueLeft` |
| 236 | `CTRL_expressions_tongueNarrow` |
| 237 | `CTRL_expressions_tongueOut` |
| 238 | `CTRL_expressions_tonguePress` |
| 239 | `CTRL_expressions_tongueRight` |
| 240 | `CTRL_expressions_tongueRoll` |
| 241 | `CTRL_expressions_tongueThick` |
| 242 | `CTRL_expressions_tongueThin` |
| 243 | `CTRL_expressions_tongueTipDown` |
| 244 | `CTRL_expressions_tongueTipLeft` |
| 245 | `CTRL_expressions_tongueTipRight` |
| 246 | `CTRL_expressions_tongueTipUp` |
| 247 | `CTRL_expressions_tongueTwistLeft` |
| 248 | `CTRL_expressions_tongueTwistRight` |
| 249 | `CTRL_expressions_tongueUp` |
| 250 | `CTRL_expressions_tongueWide` |

`getMetaHumanBlendshapeIndex(name)` and `getMetaHumanBlendshapeName(index)` convert between a full control name and its index. `METAHUMAN_CATEGORIES` maps a region name (`brows`, `ears`, `eyes`, `eyelashes`, `jaw`, `mouth`, `neck`, `nose`, `teeth`, `tongue`) to a `start`, `end`, and `count`, and `getMetaHumanBlendshapesByCategory(category)` returns the names in that range. `KEY_METAHUMAN_LIPSYNC` maps a few speech-relevant controls, such as `JAW_OPEN`, to their indexes.

## Related reference

{% content-ref url="real-time-lipsync.md" %}
[Add lip sync in vanilla TypeScript](real-time-lipsync.md)
{% endcontent-ref %}

{% content-ref url="../lipsync-and-blendshape/README.md" %}
[Drive facial animation with blendshapes](../lipsync-and-blendshape/README.md)
{% endcontent-ref %}

{% content-ref url="best-practices-and-type-definitions.md" %}
[Configuration and type reference](best-practices-and-type-definitions.md)
{% endcontent-ref %}
