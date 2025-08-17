from ultralytics import YOLO
import ultralytics
import time, os
import importlib
import torch

supported_sizes = importlib.import_module('mmcensor.const').supported_sizes

# In pytorch version >=2.6, `weights_only` argument in `torch.load` changed from `False` to `True`. 
# Therefore it's needed to add the model classes to the safe globals.
torch.serialization.add_safe_globals([ultralytics.nn.tasks.DetectionModel,
                                      torch.nn.modules.container.Sequential,
                                      ultralytics.nn.modules.conv.Conv,
                                      torch.nn.modules.conv.Conv2d,
                                      torch.nn.modules.batchnorm.BatchNorm2d,
                                      torch.nn.modules.activation.SiLU,
                                      ultralytics.nn.modules.block.C2f,
                                      torch.nn.modules.container.ModuleList,
                                      ultralytics.nn.modules.block.Bottleneck,
                                      ultralytics.nn.modules.block.SPPF,
                                      torch.nn.modules.pooling.MaxPool2d,
                                      torch.nn.modules.upsampling.Upsample,
                                      ultralytics.nn.modules.conv.Concat,
                                      ultralytics.nn.modules.head.Detect,
                                      ultralytics.nn.modules.block.DFL,
                                      ultralytics.utils.IterableSimpleNamespace,
                                      ultralytics.utils.loss.v8DetectionLoss,
                                      torch.nn.modules.loss.BCEWithLogitsLoss,
                                      ultralytics.utils.tal.TaskAlignedAssigner,
                                      ultralytics.utils.loss.BboxLoss])

t_1 = time.perf_counter()
model = YOLO( '../neuralnet_models/640m.pt' )
for size in supported_sizes:
    model.export( format='engine',imgsz=size,half=True,dynamic=True)
    os.rename( '../neuralnet_models/640m.engine', '../neuralnet_models/640m-%d.engine'%size )
t_2 = time.perf_counter()
print( t_2-t_1 )
