## DeepDetect AMI Tools

A Python productivity tool for easily managing services and pre-trained models with DeepDetect AMIs (https://deepdetect.com/products/ami/).

Below, replace 52.xx.xx.xx with your AMI public IP address.

### Server Info

```
python ddami.py --host 52.xx.xx.xx --info
```

### Service Creation

```
python ddami.py --host 52.xx.xx.xx --create --model-name googlenet
{u'status': {u'msg': u'Created', u'code': 201}}
```
Note that first service creation can take up to a minute, due to EC2 GPU initialization.

You can replace `googlenet` with any of the available models on https://deepdetect.com/products/ami/

You can check that the service is alive:

```
python ddami.py --host 52.xx.xx.xx --info
{u'status': {u'msg': u'OK', u'code': 200}, u'head': {u'services': [{u'mllib': u'caffe', u'name': u'googlenet', u'description': u'googlenet'}], u'commit': u'32e3856ab923f25907f397c52ac1b99e185ba496', u'version': u'0.1', u'method': u'/info', u'branch': u'master'}}
```

### Image Classification

```
python ddami.py --host 52.59.93.11 --model-name googlenet --img-url https://deepdetect.com/img/cat.jpg

{u'status': {u'msg': u'OK', u'code': 200}, u'body': {u'predictions': [{u'classes': [{u'prob': 0.4764571785926819, u'cat': u'n02123045 tabby, tabby cat'}, {u'prob': 0.3385276198387146, u'cat': u'n02124075 Egyptian cat'}, {u'last': True, u'prob': 0.1657179743051529, u'cat': u'n02123159 tiger cat'}], u'uri': u'https://deepdetect.com/img/cat.jpg'}]}, u'head': {u'method': u'/predict', u'service': u'googlenet', u'time': 158.0}}
```

### Service Deletion

```
python ddami.py --host 52.59.93.11 --delete --model-name googlenet

{u'status': {u'msg': u'OK', u'code': 200}}
```

You can check that the service is gone:

```
python ddami.py --host 52.59.93.11 --info

{u'status': {u'msg': u'OK', u'code': 200}, u'head': {u'services': [], u'commit': u'32e3856ab923f25907f397c52ac1b99e185ba496', u'version': u'0.1', u'method': u'/info', u'branch': u'master'}}
```

For any issue, contact us at ami@deepdetect.com
