import weaviate
import json

try:
    client = weaviate.connect_to_local()
    assert client.is_live()
    print('------connected------')

    metainfo = client.get_meta()  # hostname and embedded metadata
    print(json.dumps(metainfo, indent=2))
finally:
    # weaviate is closed and resource is released
    client.close()