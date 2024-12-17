---
description: This guide explains how to enable long term memory in Convai Character
---

# Long Term Memory

#### Steps to enable long term memory

1. Select your character in the playground on the Convai website.
2. Go to the  **Memories Tab**, and then to **Memory Settings**. Enable **Long Term Memory**  for the character there.

<figure><img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXdi0A9NklIgt-d5Ftz4NWdHNXuSgCWNqofBPo6bpu50EC2AcLXiC_BnV8m1-FTQzk2Ob9_peusElQJlNaezDucB4y0gLnq5G4a2SVR9WOqmOngvAxw7_9GK4KtTmiaXxmI_rQ9y?key=E4IGNaHrJaNNjEd9PTsNBzqR" alt=""><figcaption></figcaption></figure>

#### Steps to setup LTM in Unreal Engine

1. Go to, **Project Settings -> Plugins -> Convai**. where you have set the API key.
2. There, click on the **Manage Speaker ID**. button under **Long Term Memory.** This will spawn an editor utility to create, delete, and list speaker ids.

<figure><img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXfVOObpWqcg0mMr5Rmp0Z-ZIgF4iHBIDE_MVR6SvrVroOd18JM3Y4hjhZ752jQXYV-dRRcAyzY9Vrulh1SfRMD1umwv8CseBgc8THwoBz2o7XReIgitWENsSmiLcy2UT4YhpWS6?key=E4IGNaHrJaNNjEd9PTsNBzqR" alt=""><figcaption></figcaption></figure>

3. If you have already created a Speaker ID, you can click **List All Speaker IDs**. Then, go to **Project Settings -> Plugins -> Convai**, and under **Long Term Memory**, you will find the Speaker IDs array. Copy the desired Speaker ID.
4. Now, go to the Player Blueprint and select the ConvaiPlayer component. In the details panel, you will find a Speaker ID field under the Convai category. Past the desired Speaker ID there.

<figure><img src="../../../.gitbook/assets/image (419).png" alt=""><figcaption></figcaption></figure>
