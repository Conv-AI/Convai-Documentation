# Failure to load character IDs

When running the Convai plugin on a machine that is missing certain popular root certificates you will receive errors when trying to fetch characters' data and you will usually see this error in the chat widget `Load Failed for Character ID: <Character ID>`.

To fix the issue, you need to disable SSL verification from Unreal Engine, this can be done by going to Edit menu, select Project Settings and search for `Verify Peer` and disable it.

<figure><img src="../../../.gitbook/assets/image (413).png" alt=""><figcaption><p>Disable Verify Peer</p></figcaption></figure>

Another solution is to install any browser like Google Chrome or Fire Fox which usually install the required certificates automatically.
