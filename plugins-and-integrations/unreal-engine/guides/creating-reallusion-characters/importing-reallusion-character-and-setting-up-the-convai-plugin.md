---
description: >-
  This document explains how a Reallusion Character can be imported and used
  with the Convai Plugin.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/guides/creating-reallusion-characters/importing-reallusion-character-and-setting-up-the-convai-plugin
---

# Importing Reallusion character and setting up the Convai plugin

## Steps to import Reallusion Character and setting up with Convai Plugin: -

1. Create / open a project in Unreal Engine and download the Reallusion auto setup for Unreal Engine from this [link](https://www.reallusion.com/auto-setup/unreal-engine/default.html).
2. **`Download > install > Open a folder based on your Unreal Engine version.`**

<figure><img src="https://lh4.googleusercontent.com/KKHzQ2Tq3PFpumDUDOvUk86Vtq3_Vojbc3tQqPof8B9vSDVQd4Ef8eSzSF8vOuyfNKzdnU1kElkFKCGQ-k7opYiiCjlDTvlPAhlPVn9BP2tb2_S059-C6ZqCtD-IjnfQbSem6VOzuPNTFhp0W1xQEYQ" alt=""><figcaption><p>Select based on Unreal Engine verison </p></figcaption></figure>

3. Copy the Content and Plugins folder and paste them in your Unreal Engine project folder.

<figure><img src="https://lh6.googleusercontent.com/ELKVfBx_ahVctYmPA-QcrSf5RlUXCufeekayrh1kPiA25FN3_UhOResU1HCq3z3t7xoqKgwblMMIuU9ZOdOe-LTr7BQLqoG_nOkMdULVCChzxSTGuqqjU3gNIqLpBnbHhc1d3kFMY6_wtydYKFesQW0" alt="" width="375"><figcaption></figcaption></figure>

4. Restart your project and create a new folder (say ‘Kevin’) in your content browser.
5. Copy the **`.Fbx`** file (named as the character) from the export to `‘Kevin’` in the content browser and the FBX Import Options menu will pop up.
6.  Check the following options and click Import All :-

    * Use T0 As Ref Pose.
    * Import Morph Targets.



    <figure><img src="https://lh4.googleusercontent.com/syMmhHd9yIz8WfhSh8Vns7UrE5kbkEH37vS5duikYA_M4-O5D1IpudCcDyVtyC4hdjJUHAzbSdPWBzhKaUcX02YCbPamGcVqO9_biV2HFg4gBn5rmliCdwqY-WRsFBbsz92GtcK5Oiia3syh4TrU5JY" alt=""><figcaption></figcaption></figure>


7. Create a new folder named Animations within the Kevin folder and import all the animation file (named **‘\_motion’** at the end) from the exported file from Reallusion.

<figure><img src="https://lh3.googleusercontent.com/4g9rAlvonvdnIDFAkGIe0P9J9_m21k5TZQ6l8jV3aSX5TFKOpOo0ldHYc9dO08DZMou5PkwhBMbwgc-wlIh8juI0wt7IderaCSjTezKz8ppqNXSxDrUIdlRc-wbn0wxuKVlQlPf0kAEXUAMxmouJkd8" alt=""><figcaption><p>Examples of animation files</p></figcaption></figure>

8. The FBX Import Options pop up again and Uncheck the Import Mesh and select your imported skeleton.
9. Under **`Animation > advanced`**. Check the Use Default Sample Rate.
10. Click Import All.
11. Now install the Convai Plugin from Epic marketplace and restart the engine.
12. **`Edit > Plugins`**.
13. Search for **`‘Convai’`** and enable it by clicking the checkbox and restart.
14. Create a new Blueprint Class within Kevin folder and under ALL CLASSES select **`‘ConvaiBaseCharacter’.`**

<figure><img src="https://lh6.googleusercontent.com/eumEmsYeMLBaAeArB2TIzZNx_d1h-oaQ_xqI5KKfWGX8MdoDlACJQYrKFOtGsWbdCdqpgLWTbLiNnO7hoSumHsX0GNeaR6Wmbn6BxxeFOShKzU052DeJhttnEy432OK_aQNUsTWQjS7qygtjKk4Yo9I" alt=""><figcaption></figcaption></figure>

15. Open up the blueprint. **`Components > add > Skeletal Mesh.`**

<figure><img src="https://lh4.googleusercontent.com/1gk_tQ_A6ASsQds3SS88HMWgpWIahG_4TB-qHeg7rRJ1ZNdXa7KWPSEqmgBdK4lSmv95l4VWZuqJ8IVSu4pC4X2BQ5z1vVBCV0Syat5vdKaVcr9aNjWmP9aGJTHHfuGoJ9NFCiZJ34B_G7NVSyBF7Jo" alt="" width="375"><figcaption></figcaption></figure>

16. Under the details tab go to **`mesh > Skeletal Mesh`** and select the imported mesh named Kevin form Reallusion.

<figure><img src="https://lh6.googleusercontent.com/Ysmyg83HIUMsbTpYlxNa5KUVovd7RQR5tyDlWI0l7rT_EESRC4aZ5Z-e2nGQvB8N-NoguKxvUJ4G5EPB8Ktf6_fkzzuJGi9gSx0Lq4U4e1D3ARQ1OWfkWDwqd2ZIh1uka2Yfn0Z0GJ1kmGQhfd2miDo" alt="" width="375"><figcaption><p>Select a Mesh from dropdown menu</p></figcaption></figure>

<figure><img src="https://lh6.googleusercontent.com/jlBbvoU4jYLvmuGAUnzI1Sf1tKckWTWuRFUcAD_EBwHjT1b264smAD5Ba4PZNcWlnPn_c4RtSAl2Q8Eeh2hHBluiWKbx9S1C0PNB3YcMZeEBhKXGqcNjE0XPn_l6HIQlx5LD17oE4pJUIYsaziPuwZ0" alt="" width="188"><figcaption><p>Choose a Mesh </p></figcaption></figure>

17. To change the parent class of the player refer to [this](../creating-metahuman-characters/change-the-parent-class-for-player..md) section.
18. &#x20;Finally add the Character Id by selecting the Character (from Convai website) you just added and you can enjoy talking to your AI buddy.<br>

<figure><img src="https://lh6.googleusercontent.com/2qBxsfaY76JYx4Y_Ipm58ThbQv1cyZDQg7Kb3G9aWL9_YowEgxhrxX2ce_HlqXkgybndrdXP4w5pcOeIMEitjAUvDG5pbftlbmuRlpcd_VCRpVzgPDWQlAQc1zcE8tKCLM6cvXGnQloOee06JkJ5JaQ" alt=""><figcaption><p>Enter Character ID here</p></figcaption></figure>
