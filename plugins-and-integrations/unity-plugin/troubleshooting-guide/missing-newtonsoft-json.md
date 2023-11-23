# Missing Newtonsoft Json

Our plugin has various scripts and dependencies that use Newtonsoft Json. If Newtonsoft Json is missing from the plugin, it could lead to a large number of errors as shown below:

<figure><img src="../../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

Ensure that NewtonSoft.Json is present in your packages. Go to your project folder.&#x20;

<figure><img src="../../../.gitbook/assets/image (185).png" alt=""><figcaption></figcaption></figure>

Then navigate to Packages folder. In the Packages folder. Click on manifest.json. A json file containing the project dependacies should open up.

Add the Newtonsoft Json Package on top.

```json
"com.unity.nuget.newtonsoft-json": "3.0.2",
```

The final manifest.json should look like this.

```json
{  
    "dependencies": {
        "com.unity.nuget.newtonsoft-json": "3.0.2", 
        "com.unity.animation.rigging": "1.1.1",
        "com.unity.ide.rider": "3.0.16",
        "com.unity.ide.visualstudio": "2.0.16",
        "com.unity.ide.vscode": "1.2.5",
        "com.unity.test-framework": "1.1.33",
        "com.unity.textmeshpro": "3.0.6",
        "com.unity.timeline": "1.6.4",
        .
        .
        .
    }
}
```
