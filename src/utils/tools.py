from src.utils import cycle
import cv2
import os

drawing = False  
color = (255, 255, 255)
color_outside = (255, 255, 255)  # Cross-hair color
radius = 30 
ix, iy = -1, -1  

def putText(img, text, position):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 0.5
    cv2.putText(img, text, position, font, font_size, ( 0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(img, text, position, font, font_size, (255,255, 255), 1, cv2.LINE_AA)

def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

    elif event == cv2.EVENT_MOUSEMOVE:
        ix, iy = x, y

def pass_img(model_callback, reshape, forward=True):
    global img, mask_img, actual_filename, original_shape

    actual_filename = images_filenames.next() if forward else images_filenames.previous()
    mask_filename = actual_filename.replace('jpg', 'png')

    img = cv2.imread(os.path.join(input_image_path, actual_filename))
    original_shape = img.shape[:2]

    if model_callback:
        mask_img = model_callback(img)
    mask_img = cv2.imread(os.path.join(output_mask_path, mask_filename))

    if reshape:
        img = cv2.resize(img, reshape)
        mask_img = cv2.resize(mask_img, reshape)

def save_img(reshape):
    if reshape:
        resized_mask = cv2.resize(mask_img, original_shape)
        cv2.imwrite(os.path.join(output_mask_path, actual_filename.replace('jpg', 'png')), resized_mask)
    else:
        cv2.imwrite(os.path.join(output_mask_path, actual_filename.replace('jpg', 'png')), mask_img)

def run(BASE_PATH, reshape=None, model_callback=None):
    global images_filenames, input_image_path, output_mask_path, radius, color, color_outside

    saved = False
    input_image_path = f"{BASE_PATH}/imgs"
    output_mask_path = f"{BASE_PATH}/masks"

    images_filenames = os.listdir(input_image_path)

    assert len(images_filenames) > 0, f"No images found in the {input_image_path} folder"

    images_filenames.sort()

    images_filenames = cycle.Iter(images_filenames)

    pass_img(model_callback, reshape)
    print(mask_img)
    cv2.namedWindow('Labeling')
    cv2.setMouseCallback('Labeling', draw_circle)

    while True:

        if drawing:
            cv2.circle(mask_img, (ix, iy), radius, color, -1)

        # Adiciona a imagem original com a imagem temporária com círculo usando addWeighted
        res = cv2.addWeighted(img, 0.5, mask_img, 0.5, 1.0)

        # CrossHair do Mouse
        cv2.circle(res, (ix, iy), radius, color_outside, 1)
        
        # Adicione os textos de referência
        putText(res, f'File: {actual_filename}', (10,30))
        putText(res, f'Radius: {radius}  C + | V -', (10,50))
        putText(res, f'Ferramenta (D | F): {"Draw" if color == (255,255,255) else "Erase"}', (10,70))
        putText(res, f'Labeled (S): {"Yes" if saved else "No"}  ', (10,90))
        putText(res, f'Change Image: << O | P >>', (10,110))

        # Mostra a imagem
        cv2.imshow('Labeling', res)
        key = cv2.waitKey(1)
        # Pressionar Q encerra a segmentação
        if key & 0xFF == ord('q'):
            break
        
        # Pressionar C aumenta o raio da seleção da mascara 
        if key & 0xFF == ord('c'):
            radius += 3
        
        # Pressionar V diminui o raio de seleção
        if key & 0xFF == ord('v'):
            radius -= 3
        
        # Pressionar D alternar para a ferramenta de adição a segmentação 
        if key & 0xFF == ord('d'):
            color = (255, 255, 255)
            color_outside = (255, 255, 255)
        
        # Pressionar F alterna para a ferramenta de remoção a segmentação
        if key & 0xFF == ord('f'):
            color = (0, 0, 0)
            color_outside = (0, 0, 255)

        # Pressionar S salva a imagem da segmentação
        if key & 0xFF == ord('s'):
            saved = True
            save_img(reshape)
        
        if key & 0xFF == ord('p'):
            saved = False
            pass_img(model_callback, reshape)

        if key & 0xFF == ord('o'): 
            saved = False
            pass_img(model_callback, reshape, forward=False)
            
    cv2.destroyAllWindows()