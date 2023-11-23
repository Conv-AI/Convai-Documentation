# Compatibility

## Development Operating System

You can only develop the corresponding versions of the Convai Unity Plugin based on your preferred operating system.

<table><thead><tr><th width="208.33333333333331">Operating System</th><th>Compatible Unity Plugin Versions</th><th>Notes</th></tr></thead><tbody><tr><td>Windows</td><td>Core, Complete</td><td></td></tr><tr><td>Mac</td><td>Core, Complete</td><td>Requires you to allow access to the "grpc_csharp_ext.bundle" from Privacy &#x26; Security settings.</td></tr><tr><td>Linux</td><td>N/A</td><td>Untested on Unity for Linux</td></tr><tr><td>WebGL</td><td>WebGL</td><td></td></tr></tbody></table>

## Unity Version[​](https://docs.inworld.ai/docs/tutorial-integrations/Unity/get-started/compatibility#unity-version) <a href="#unity-version" id="unity-version"></a>

<table><thead><tr><th width="159">Unity Version</th><th width="147">Tested Version</th><th width="444">API Level</th></tr></thead><tbody><tr><td>2020.3</td><td>2020.3.34f1</td><td>.NET 4.x Only</td></tr><tr><td>2021.1</td><td>2021.1.21f1</td><td>.NET 4.x Only</td></tr><tr><td>2021.2</td><td>2021.2.0f1</td><td>.NET Standard 2.1 or .NET Framework</td></tr><tr><td>2021.3</td><td>2021.3.2f1</td><td>.NET Standard 2.1 or .NET Framework</td></tr><tr><td>2022.1</td><td>2022.1.24f1</td><td>.NET Standard 2.1 or .NET Framework</td></tr><tr><td>2022.2</td><td>2022.2.11f1</td><td>.NET Standard 2.1 or .NET Framework</td></tr></tbody></table>

## Disabling Assembly Validation

If you ever get an error that looks like this, disable the Assemble Version Validation in `Project Settings` > `Player` > `Other Settings`.

{% code overflow="wrap" %}
```
Assembly 'Assets/Convai/Plugins/Grpc.Core.Api/lib/net45/Grpc.Core.Api.dll' will not be loaded due to errors: 
Grpc.Core.Api references strong named System.Memory Assembly references: 4.0.1.1 Found in project: 4.0.1.2.
```
{% endcode %}

<figure><img src="https://docs.inworld.ai/assets/images/AssemblyValidate-dc01f14967253df8fc95c74a92a43f12.png" alt=""><figcaption></figcaption></figure>

## Platform[​](https://docs.inworld.ai/docs/tutorial-integrations/Unity/get-started/compatibility#platform) <a href="#platform" id="platform"></a>

Other platforms will be tested and updated shortly.

| Tested Platform | Scripting Backend | API Level                      |
| --------------- | ----------------- | ------------------------------ |
| Windows         | MONO              | .NET Standard 2.1 or .NET 4.x+ |
| Android         | IL2CPP            | .NET 4.x                       |
| Oculus          | IL2CPP            | .NET 4.x                       |
