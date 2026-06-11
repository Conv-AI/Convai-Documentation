---
title: File upload platform examples
description: Upload images to Convai from JavaScript, React Native, Swift for iOS, and Kotlin for Android using the LiveKit byte-stream channel.
last_reviewed: "2026-06-11"
---

The following examples show the `sendFile` call for each supported platform. Each example assumes an active LiveKit room connection is already established before the upload is initiated. For step-by-step setup, see [Upload an image](upload-an-image.md).

{% tabs %}
{% tab title="JavaScript / TypeScript" %}
```typescript
import { Room } from "livekit-client";

const room = new Room();
await room.connect(LIVEKIT_SERVER_URL, YOUR_LIVEKIT_TOKEN);

// Upload an image file
async function uploadImage(file: File) {
  try {
    const info = await room.localParticipant.sendFile(file, {
      topic: "file-upload", // Required: must match server topic
      mimeType: file.type,

      // Optional: track upload progress
      onProgress: (progress) => {
        console.log(`Upload progress: ${Math.ceil(progress * 100)}%`);
      },
    });

    console.log(`Uploaded file with stream ID: ${info.id}`);
  } catch (error) {
    console.error("Upload failed:", error);
  }
}

// Example: Upload from file input
const fileInput = document.querySelector("#file-input") as HTMLInputElement;
fileInput.addEventListener("change", async (e) => {
  const file = fileInput.files?.[0];
  if (file && file.type.startsWith("image/")) {
    await uploadImage(file);
  } else {
    console.error("Please select an image file");
  }
});
```
{% endtab %}

{% tab title="React Native" %}
```typescript
import { Room } from "@livekit/react-native";
import DocumentPicker from "react-native-document-picker";
import { readFile } from "react-native-fs";

async function uploadImageFromDevice(room: Room) {
  try {
    // Pick image from device
    const result = await DocumentPicker.pickSingle({
      type: [DocumentPicker.types.images],
    });

    // Read file data
    const fileData = await readFile(result.uri, "base64");
    const blob = new Blob([Buffer.from(fileData, "base64")], {
      type: result.type,
    });

    // Upload to LiveKit
    const info = await room.localParticipant.sendFile(blob, {
      topic: "file-upload",
      mimeType: result.type,
    });

    console.log("Image uploaded:", info.id);
  } catch (error) {
    console.error("Upload failed:", error);
  }
}
```
{% endtab %}

{% tab title="Swift (iOS)" %}
{% hint style="info" %}
The Swift LiveKit SDK passes the topic as the `for:` argument label rather than inside an options struct. Pass `"file-upload"` as the `for:` value.
{% endhint %}

```swift
import LiveKit
import UIKit

func uploadImage(_ imageURL: URL, room: Room) async throws {
    do {
        let info = try await room.localParticipant.sendFile(
            imageURL,
            for: "file-upload"  // Required topic
        )
        print("Uploaded file with stream ID: \(info.id)")
    } catch {
        print("Upload failed: \(error)")
        throw error
    }
}

// Example: Upload from UIImagePickerController
class ImageUploadViewController: UIViewController, UIImagePickerControllerDelegate {
    var room: Room?

    func imagePickerController(
        _ picker: UIImagePickerController,
        didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]
    ) {
        guard let imageURL = info[.imageURL] as? URL,
              let room = room else { return }

        Task {
            try await uploadImage(imageURL, room: room)
        }
    }
}
```
{% endtab %}

{% tab title="Kotlin (Android)" %}
```kotlin
import io.livekit.android.room.Room
import java.io.File

suspend fun uploadImage(imageFile: File, room: Room) {
    val result = room.localParticipant.sendFile(
        imageFile,
        StreamBytesOptions(topic = "file-upload")
    )

    result.onSuccess { info ->
        Log.i("Upload", "Uploaded file: ${info.id}")
    }.onFailure { error ->
        Log.e("Upload", "Upload failed", error)
    }
}

// Example: Upload from file picker
class ImageUploadActivity : AppCompatActivity() {
    private lateinit var room: Room

    private val pickImage = registerForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let { handleImageSelection(it) }
    }

    private fun handleImageSelection(uri: Uri) {
        val file = File(getRealPathFromURI(uri))

        lifecycleScope.launch {
            uploadImage(file, room)
        }
    }

    fun openImagePicker() {
        pickImage.launch("image/*")
    }
}
```
{% endtab %}
{% endtabs %}

## Platform API differences

The `sendFile` API signature varies between platforms. The JavaScript and React Native implementations accept an options object with a `topic` property. The Swift LiveKit SDK passes the topic as the `for:` named argument — there is no options struct. The Kotlin Android SDK wraps options in a `StreamBytesOptions` type with a `topic` constructor parameter.

All four implementations produce the same server-side behavior when `topic` is `"file-upload"`.

## Next steps

For the full parameter contract and response fields, see the reference.

{% content-ref url="file-upload-reference.md" %}
[File upload reference](file-upload-reference.md)
{% endcontent-ref %}

If an upload fails or produces no response, see the troubleshooting guide.

{% content-ref url="troubleshooting.md" %}
[Troubleshoot file upload](troubleshooting.md)
{% endcontent-ref %}
