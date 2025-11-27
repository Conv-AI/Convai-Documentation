---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin/troubleshooting-guide/enabled-assembly-validation
---

# Disable Assembly Validation

If you ever get an error that looks like this, disable the Assemble Version Validation in `Project Settings` > `Player` > `Other Settings`.

{% code overflow="wrap" %}
```
Assembly 'Assets/Convai/Plugins/Grpc.Core.Api/lib/net45/Grpc.Core.Api.dll' will not be loaded due to errors: 
Grpc.Core.Api references strong named System.Memory Assembly references: 4.0.1.1 Found in project: 4.0.1.2.
```
{% endcode %}

Ensure that Assembly Validation is disabled in `Project Settings` > `Player` > `Other Settings`.

<figure><img src="https://docs.inworld.ai/assets/images/AssemblyValidate-dc01f14967253df8fc95c74a92a43f12.png" alt=""><figcaption></figcaption></figure>

Restart the Unity project after unchecking the box should fix the issue.
