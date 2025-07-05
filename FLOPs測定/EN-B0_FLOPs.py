from ptflops import get_model_complexity_info
import torchvision.models as models

# EfficientNet-B0 モデルの読み込み
model = models.efficientnet_b0()

# FLOPs・パラメータ数の測定
macs_str, params_str = get_model_complexity_info(
    model, (3, 224, 224), as_strings=True, print_per_layer_stat=False
)

# "410.2 MMac" → 数値だけ抽出し、2倍して GFLOPs に変換
macs_value = float(macs_str.split()[0])  # '410.2'
flops_gflops = (macs_value * 2) / 1000  # MAC × 2 / 1000 = GFLOPs
flops_str = f"{flops_gflops:.3f} GFLOPs"

print(f"FLOPs: {flops_str}")
print(f"Params: {params_str}")
