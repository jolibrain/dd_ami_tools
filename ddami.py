import os, sys, argparse
from dd_client import DD

base_path_caffe = '/opt/deepdetect/models/base/caffe/'
base_path_tf = '/opt/deepdetect/models/base/tf/'
extra_path_caffe = '/opt/deepdetect/models/apps/caffe/'

models_config = {
    'googlenet': {'backend':'caffe','nclasses':1000,'width':224,'height':224,'path':base_path_caffe},
    'inception_v1': {'backend':'tensorflow','nclasses':1000,'width':224,'height':224,'path':base_path_tf},
    'inception_v2': {'backend':'tensorflow','nclasses':1001,'width':224,'height':224,'path':base_path_tf},
    'inception_v3': {'backend':'tensorflow','nclasses':1001,'width':299,'height':299,'path':base_path_tf},
    'resnet_50': {'backend':'caffe','nclasses':1000,'width':299,'height':299,'path':base_path_caffe},
    'resnet_101': {'backend':'caffe','nclasses':1000,'width':299,'height':299,'path':base_path_caffe},
    'resnet_152': {'backend':'caffe','nclasses':1000,'width':299,'height':299,'path':base_path_caffe},
    'inception_resnet_v2': {'backend':'tensorflow','nclasses':1001,'width':299,'height':299,'path':base_path_tf},
    'openimages_inception_v3': {'backend':'tensorflow','nclasses':6012,'width':299,'height':299,'path':base_path_tf},
    'voc0712': {'backend':'caffe','nclasses':23,'widht':300,'height':300,'path':base_path_caffe},
    # extra
    'age_model': {'backend':'caffe','nclasses':8,'width':224,'height':224,'path':base_path_caffe},
    'gender': {'backend':'caffe','nclasses':2,'width':224,'height':224,'path':base_path_caffe},
    'clothing': {'backend':'caffe','nclasses':304,'width':224,'height':224,'path':base_path_caffe},
    'fabric': {'backend':'caffe','nclasses':233,'width':224,'height':224,'path':base_path_caffe},
    'buildings': {'backend':'caffe','nclasses':185,'width':224,'height':224,'path':base_path_caffe},
    'bags': {'backend':'caffe','nclasses':37,'width':224,'height':224,'path':base_path_caffe},
    'footwear': {'backend':'caffe','nclasses':51,'width':224,'height':224,'path':base_path_caffe},
    'sports': {'backend':'caffe','nclasses':143,'width':224,'height':224,'path':base_path_caffe},
    'furnitures': {'backend':'caffe','nclasses':179,'width':224,'height':224,'path':base_path_caffe},
}

parser = argparse.ArgumentParser()
parser.add_argument('--host',help='AMI public IP')
parser.add_argument('--model-name',help='model name, e.g. googlenet, resnet_50, age_model, gender, clothing, see https://deepdetect.com/products/ami/ for full list',default='googlenet')
parser.add_argument('--info',help='simple info call to remote DeepDetect server',action='store_true')
parser.add_argument('--create-service',help='whether to create service',action='store_true')
parser.add_argument('--delete',help='wether to delete service',action='store_true')
parser.add_argument('--img-url',help='URL of image to classify')
args = parser.parse_args()

host = args.host
dd = DD(host,8080)
dd.set_return_format(dd.RETURN_PYTHON)

if not args.model_name in models_config:
    print('Unknown model=',args.model_name)
    sys.exit()

model_config = models_config[args.model_name]

# info call
if args.info:
    info = dd.info()
    print(info)
    sys.exit()

if args.delete:
    delete_service = dd.delete_service(args.model_name,clear='')
    print(delete_service)
    sys.exit()
    
# creating ML service
if args.create_service:
    model = {'repository':model_config['path']+args.model_name}
    parameters_input = {'connector':'image','width':model_config['width'],'height':model_config['height']}
    parameters_mllib = {'nclasses':model_config['nclasses'],'gpu':True}
    parameters_output = {}
    creation = dd.put_service(args.model_name,model,args.model_name,model_config['backend'],
                              parameters_input,parameters_mllib,parameters_output,'supervised')
    print(creation)

if args.img_url:
    parameters_input = {}
    parameters_mllib = {}
    parameters_output = {'best':3}
    if args.model_name == 'voc0712':
        parameters_output['bbox'] = True
        parameters_output['confidence_threshold'] = 0.01
    data = [args.img_url]
    classify = dd.post_predict(args.model_name,data,
                               parameters_input,parameters_mllib,parameters_output)
    print classify
