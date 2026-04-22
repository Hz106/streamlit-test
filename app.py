import streamlit as st
import numpy as np
from PIL import Image

# 色盲模拟转换矩阵
matrices = {
    "正常视觉 (Normal)": np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]),
    "红色盲 (Protanopia)": np.array([
        [0.567, 0.433, 0],
        [0.558, 0.442, 0],
        [0, 0.242, 0.758]
    ]),
    "绿色盲 (Deuteranopia)": np.array([
        [0.625, 0.375, 0],
        [0.7, 0.3, 0],
        [0, 0.3, 0.7]
    ]),
    "蓝色盲 (Tritanopia)": np.array([
        [0.95, 0.05, 0],
        [0, 0.433, 0.567],
        [0, 0.475, 0.525]
    ]),
    "全色盲 (Achromatopsia)": np.array([
        [0.299, 0.587, 0.114],
        [0.299, 0.587, 0.114],
        [0.299, 0.587, 0.114]
    ])
}

def apply_filter(image, matrix):
    """应用色彩转换矩阵"""
    # 将 PIL 图像转换为 numpy 数组
    img_array = np.array(image)
    
    # 检查图片是否有 alpha 通道 (RGBA)
    has_alpha = img_array.shape[-1] == 4
    
    if has_alpha:
        rgb = img_array[:, :, :3]
        alpha = img_array[:, :, 3:]
    else:
        rgb = img_array[:, :, :3]
        
    # 应用矩阵乘法
    # np.dot 会将 rgb (H, W, 3) 与 matrix.T (3, 3) 运算，得到 (H, W, 3)
    new_rgb = np.dot(rgb, matrix.T)
    
    # 限制像素值在 0-255 范围内，并转换为 uint8 类型
    new_rgb = np.clip(new_rgb, 0, 255).astype(np.uint8)
    
    # 重新拼接 alpha 通道（如果有）
    if has_alpha:
        new_img_array = np.concatenate((new_rgb, alpha), axis=-1)
    else:
        new_img_array = new_rgb
        
    return Image.fromarray(new_img_array)

def main():
    st.set_page_config(page_title="视觉模拟 - 色盲视界", page_icon="👁️", layout="centered")
    
    st.title("👁️ 色盲视界模拟器")
    st.markdown("从医学视角，探索不同的视觉世界。请上传一张图片，并选择对应的色觉类型进行模拟。")
    
    # 图片上传组件
    uploaded_file = st.file_uploader("点击或拖拽上传图片", type=['png', 'jpg', 'jpeg', 'webp'])
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            
            st.markdown("---")
            st.subheader("选择视觉类型")
            
            # 视觉类型单选按钮
            option = st.radio(
                "请选择您想要模拟的色盲类型：",
                list(matrices.keys()),
                horizontal=True
            )
            
            st.markdown("---")
            
            # 使用 spinner 显示处理状态
            with st.spinner("正在通过矩阵运算重构色彩..."):
                filtered_image = apply_filter(image, matrices[option])
            
            # 使用两列并排对比展示
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### 原始图片")
                st.image(image, use_container_width=True)
            with col2:
                st.markdown(f"##### {option}")
                st.image(filtered_image, use_container_width=True)
                
        except Exception as e:
            st.error(f"处理图片时发生错误：{e}")

if __name__ == "__main__":
    main()