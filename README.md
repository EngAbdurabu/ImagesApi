# 🖼️ Image Processing API with Flask

A simple and powerful image processing API built with Flask and deployed on Render. It supports uploading, resizing, rotating, flipping, applying filters, and converting images to Android icon formats.

---

## 🌐 Live Demo

Base URL: [https://imagesapi-1.onrender.com](https://imagesapi-1.onrender.com)

---

## 📦 Features

- Upload and store images
- Resize images (custom or preset)
- Rotate and flip images
- Apply filters: blur, brightness, contrast
- Convert image to Android icon formats
- Simple HTTP interface

---

## 🛠️ API Endpoints

### 📤 Upload Image

**POST** `/images`

Uploads an image to the server.

**Form-Data:**

- `image`: The image file

---

### 🖼️ List Uploaded Images

**GET** `/images`

Returns a list of uploaded images with links.

---

### ✂️ Resize Image

**POST** `/actions/resize`

Resize image to custom width and height.

**Form-Data:**

- `image`: Image file
- `width`: Target width (int)
- `height`: Target height (int)

---

### 📏 Resize with Presets

**POST** `/actions/preset`

Resize image using predefined presets.

**Form-Data:**

- `image`: Image file
- `size`: One of: `small`, `medium`, `large`

---

### ↻ Rotate Image

**POST** `/actions/rotate`

Rotate the image by a specific angle.

**Form-Data:**

- `image`: Image file
- `angle`: Degrees (e.g., `90`, `180`)

---

### ↔️ Flip Image

**POST** `/actions/flip`

Flip image vertically or horizontally.

**Form-Data:**

- `image`: Image file
- `direction`: Either `horizontal` or `vertical`

---

### 🌫️ Blur Image

**POST** `/filter/blur`

Apply blur effect to the image.

**Form-Data:**

- `image`: Image file
- `radius`: Blur radius (float)

---

### 🌞 Brightness Filter

**POST** `/filter/brightness`

Adjust image brightness.

**Form-Data:**

- `image`: Image file
- `level`: Brightness level (e.g., `1.0`, `1.5`)

---

### 🌗 Contrast Filter

**POST** `/filter/contrast`

Adjust image contrast.

**Form-Data:**

- `image`: Image file
- `level`: Contrast level (e.g., `1.2`, `0.8`)

---

### 🤖 Convert to Android Icon Set

**POST** `/android`

Converts uploaded image to Android icon formats.

**Form-Data:**

- `image`: Image file

---

## 🧪 Example (using Postman or curl)

```bash
curl -X POST https://imagesapi-1.onrender.com/images \
  -F "image=@myphoto.jpg"
```
