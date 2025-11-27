---
description: This problem arises when ConvaiOVRLipSync is not added to the project.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/troubleshoot-guide/convai-module-not-found
---

# Convai Module Not Found

<figure><img src="../../../.gitbook/assets/image (353).png" alt=""><figcaption><p>Convai not found </p></figcaption></figure>

### There are two ways to resolve this issue.

1.  **Convert your Blueprint project to a C++ project.** \
    \
    Steps to convert: -&#x20;

    * &#x20;Navigate to the **Tools** menu, and choose '**New C++ class..**.' from the provided options.



    <figure><img src="https://lh7-us.googleusercontent.com/lFg-58sOnXwoA0ymQpcLKwhLzf14HdUzw5ZzencTViFdyAw2ruMkn90bsqi-C3suHaupL8jPOcl2JhHOwElUe7HigJSL2-UkZ5Mnsy2iazuy4PycgGsMI8RHFaVVtF2hMD5D02osuWrp7RTjtXIJGBU" alt=""><figcaption></figcaption></figure>

    * Select any parent class from the menu that appears. For simplicity, we opt for '**None'** in this case. Proceed by clicking on '**Next'**.



    <figure><img src="https://lh7-us.googleusercontent.com/ePdMZ3eW9UKr5cfPgnxlAX9wKaRH6OqDWJ1u5-BSn21dp0DBB1nGqj0_5stzSwHbhx97ZDxC6uB1kSOk6f-l8agP1OTkcwq0IiFQM8xTm5v_0o2gKjuL_fiBO_8epelJcgkDCsoA30pkfl5hYzK0LjE" alt=""><figcaption></figcaption></figure>

    * Provide any name and proceed by selecting '**Create Class**'.



    <figure><img src="https://lh7-us.googleusercontent.com/z9VSostmo2S_CugdG1Swc96Gk5eJR5_7l-oMS7XLZxEOZsttB3TNe_FC50RTV0xIIf4BhfVcp7PTz8odO4S5-MH4T79VmHL-RsFnr4o530dUcEt5Oi5u1d-7wD0EQ_picOUCyCj2aoCIwOoo3gLQl9k" alt=""><figcaption></figcaption></figure>

    * Once done, close the Unreal Engine editor and then start it again by clicking on build project in Microsoft Visual Studio code.


2. **Copy the ConvaiOVRLipSync plugin to the Plugins directory within the engine.**
   * **Refer to this** [<mark style="color:green;">**section**</mark>](../guides/creating-metahuman-characters/adding-lipsync-to-metahuman.md) **to add CovnaiOVRLipSync.**&#x20;



