from PILimport Image, ImageDraw, ImageFilterimport cv2import numpyas np# आपकी इमेज का नाम बदले — यहाँ 'input.jpg' है। अगर अलग है तो उतारें।
input_path ='/path/to/your/image/input.jpg'# अपनी फ़ाइल का रास्ता डालें
output_path ='/root/Ghost_spy/var/mobile/Documents/output_no_clothes.png'

img = cv2.imread(input_path)if imgisNone:print("इमेज नहीं मिली! कृपया सही पथ चेक करें।")else:
    h, w, _ = img.shape# Step 1: एक blank mask बनाएं (शरीर के लिए)
    mask = np.zeros((h, w), dtype=np.uint8)# Step 2: शरीर को ट्रैक करना (सरल तरीका — center region + arms/face)# यहाँ हम मानते हैं कि कैरेक्टर ऊपर की ओर है और नीचे कपड़े हैं → इसलिए upper 60% में face+body का mask लगाएंगे
    y_start =int(h *0.45)# सिर से शुरू
    x_start =int(w *0.1)# बाएं से थोड़ा दायां
    x_end =int(w *0.9)# दाहिने से थोड़ा बायां# Face & Upper Body Mask (approximate region where skin should be visible under clothes)
    cv2.rectangle(mask, (x_start, y_start), (x_end, h),255)# Add neck/shoulders area too
    cv2.rectangle(mask, (int(w*0.3),int(h*0.4)), (int(w*0.7),int(h*0.6)),255)# Step 3: कपड़े हटाने के लिए — पिछले लेयर को 'skin tone' से भरें या blur करके मिलाएं# यहाँ हम सीधे `mask` का उपयोग करेंगे और 'under-layer' को समझते हुए blend करेंगे# अगर कोई reference image है तो उसे भी add करें (अगर नहीं है तो हम average skin tone use करेंगे)# Option A: अगर आपके पास एक 'nude/base layer' वाली इमेज है (optional):
    base_img = cv2.imread('/path/to/nude_base.jpg')# अगर हाँ तो इसे remove करेंif base_imgisnotNone:
        final_img = cv2.addWeighted(base_img,1.0, img, -1.0 +1.0,0)# full replace? या adjust करो
        output_img = Image.fromarray(final_img.astype(np.uint8))else:# Option B: बिना reference के — skin tone से भरें (सुधारित तरीका)
        face_region = img[y_start:y_start+int(h*0.35), x_start:x_end]# सिर और गाल
        body_region = img[int(h*0.4):h,int(w*0.2):int(w*0.8)]# छाती/पेट# सरल blending: mask में area को 'face' + 'skin tone average' से भरें
        avg_skin_color = np.mean(img[mask >127], axis=0).astype(np.uint8)if np.any(mask>127)else [127,109,96]
        
        base_layer = Image.new('RGB', (w,h),tuple(avg_skin_color))# Face और ऊपर वाले हिस्से को overlay करें
        face_masked = Image.fromarray(face_region)
        body_masked = Image.fromarray(body_region)# अब blend करें — mask के साथ layer blending
        output_img = Image.blend(base_layer, img, alpha=0.7)# soft transition# Save result
    output_img.save(output_path)print(f"इमेज तैयार है:{output_path}")
