---
description: >-
  Review groom, hair, and skin settings for uploaded MetaHumans under Avatar
  Studio's target rendering profile.
---

# MetaHuman Hair and Skin Appearance Guidelines

Avatar Studio uses a supplied target rendering profile with Lumen and hardware ray tracing disabled. Tune and approve the character in that profile, because values chosen under a different renderer or lighting setup may not produce the same result.

{% hint style="info" %}
The examples on this page show one character under one lighting setup. They demonstrate the effect of each control and are not recommended default values. Change one setting at a time and judge the result on your own character.
{% endhint %}

### Before editing

* Create character-specific material instances and duplicate shared groom assets before changing them. Avoid editing shared master or plugin assets directly.
* Keep a reference image from the target camera and lighting so you can compare changes consistently.
* Use these settings for renderer compatibility and appearance calibration. They do not replace the performance guidance in the parent upload guide.

### Groom rendering settings

![Groom Hair Attributes showing Use Hair Raytracing Geometry, Voxelize, Use Stable Rasterization, and Hair Shadow Density controls.](https://413558230-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FEtUJA212Zc1S9ACc8T4l%2Fuploads%2FoQdcQeEza4Y5gEtY6YzQ%2Fgroom-attributes.png?alt=media\&token=c4cf59a0-064f-4867-b71d-5d49f8d3af29)

* **Use Hair Raytracing Geometry:** Set this to **Off** for the supplied Convai target profile. This option is relevant only when hardware ray tracing is enabled; otherwise it provides no target-renderer benefit.
* **Voxelize:** Keep this **On** in the supplied profile because it supports groom shadows and environment occlusion. **Hair Shadow Density** controls the voxel representation and will not have its intended effect when Voxelize is off.
* **Use Stable Rasterization:** Evaluate this for each groom while the character and camera are moving. Enable it when small or scattered strands alias or flicker, then check that it does not make the hair look unnaturally thick.
* **Hair Shadow Density:** Tune the voxelized shadow and transmission response under the target lighting. Treat the value as character-specific.

### Hair material settings

![Hair material parameter panel showing melanin, roughness, variation, specular, and white-hair controls.](https://413558230-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FEtUJA212Zc1S9ACc8T4l%2Fuploads%2FveXZThM4BY9iN88YGBSU%2Fhair-material-controls.png?alt=media\&token=a2da66ad-6902-41b2-86a9-50eafac59cfd)

{% hint style="warning" %}
The control screenshot shows where the parameters are located. Its displayed values are not recommendations.
{% endhint %}

* **Melanin** controls pigment and perceived hair color. Higher values generally produce darker hair.
* **Roughness** controls the breadth and softness of the hair highlights.
* **Spec0, Spec1, SpecEdge, and SpecFront** control the material's highlight lobes and directionality. Adjust them after establishing the target lighting and roughness.
* **Melanin Variation Fine and Rough** add color variation. Use them conservatively unless stronger multitone clumping is intentional.
* In the supplied material version, enable the **WhiteMelaninHigh** and **WhiteMelaninLow** parameter overrides before tuning **White Amount** for white or grey hair.

#### Melanin example

{% columns %}
{% column width="50%" %}
**Lower melanin in this example**

![Example MetaHuman with lower melanin, producing very light hair.](https://413558230-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FEtUJA212Zc1S9ACc8T4l%2Fuploads%2Fq130d2WSC44iQZ3z5Uf3%2Fhair-melanin-lower-example.png?alt=media\&token=2da352ae-c80b-4b2a-b004-b2cf31d38de4)
{% endcolumn %}

{% column width="50%" %}
**Higher melanin in this example**

![The same MetaHuman with higher melanin, producing darker brown hair.](https://413558230-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FEtUJA212Zc1S9ACc8T4l%2Fuploads%2FzfJHcqFBvFSjyp7aVzoQ%2Fhair-melanin-higher-example.png?alt=media\&token=389e92fb-bfb9-4a46-b0ac-85cda935945e)
{% endcolumn %}
{% endcolumns %}

The only intended comparison here is the visible change in pigment. Choose a value for the character and target lighting rather than copying the example.

#### Roughness example

{% columns %}
{% column width="50%" %}
**Lower roughness in this example**

![Example hair with lower roughness and sharper, brighter highlights.](https://413558230-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FEtUJA212Zc1S9ACc8T4l%2Fuploads%2FxxCHLuV5tBNNQpejMSmA%2Fhair-roughness-lower-example.png?alt=media\&token=92318ef2-0543-46b2-9a26-232b29482b4f)
{% endcolumn %}

{% column width="50%" %}
**Higher roughness in this example**

![The same hair with higher roughness and broader, softer highlights.](https://413558230-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FEtUJA212Zc1S9ACc8T4l%2Fuploads%2FIIHOFlvvmpNktiyudDN3%2Fhair-roughness-higher-example.png?alt=media\&token=69afc5e6-1cb9-423e-82c4-c634255cfc1e)
{% endcolumn %}
{% endcolumns %}

If highlights remain too strong after adjusting roughness, also review the specular controls, lighting, and exposure.

### Skin material settings

![Skin material parameter panel showing roughness and specular controls.](https://413558230-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FEtUJA212Zc1S9ACc8T4l%2Fuploads%2FDdc7aV9AGDhT6IL4DVfH%2Fskin-material-controls.png?alt=media\&token=3e06448c-f5eb-4a7e-a66b-489e70b2414c)

{% hint style="warning" %}
Material names and available controls can differ between MetaHuman and project versions. Use the controls in the supplied project and edit roughness and specular separately.
{% endhint %}

Renderer, reflection, lighting, and exposure differences can change the perceived skin gloss. Revalidate the material in the target profile instead of copying values from another renderer.

#### Skin roughness example

{% columns %}
{% column width="50%" %}
**Lower roughness in this example**

![Example MetaHuman skin with lower roughness and a glossier appearance.](https://413558230-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FEtUJA212Zc1S9ACc8T4l%2Fuploads%2F6BOMuzHAf1Jg8p89zOxq%2Fskin-roughness-lower-example.png?alt=media\&token=2ce4b9b5-7582-4887-b61c-5553f6b895c9)
{% endcolumn %}

{% column width="50%" %}
**Higher roughness in this example**

![The same MetaHuman skin with higher roughness and a less glossy appearance.](https://413558230-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FEtUJA212Zc1S9ACc8T4l%2Fuploads%2F8fcqrgefwaxaU0ddQ4rD%2Fskin-roughness-higher-example.png?alt=media\&token=24c5f95e-544f-4456-b659-63cff2f9a7b0)
{% endcolumn %}
{% endcolumns %}

### Final review

Before approving the character:

* Check the groom while the character and camera are moving.
* Review hair depth, color, and highlights under the intended lighting.
* Check the face for excessive or insufficient gloss.
* Change one control at a time so its effect remains clear.
* Review the final character in Avatar Studio before publishing it.
