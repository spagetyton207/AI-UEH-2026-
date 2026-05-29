import numpy as np
import tensorflow as tf
from keras import Sequential
from keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path

# Hệ thống ánh xạ kết quả phân loại từ CNN (41 ID) sang thông điệp text
fortune_telling_db = {
    '001': "Chỉ tay cho thấy bạn có tư duy cấu trúc cực tốt, rất hợp với các mảng phân tích dữ liệu lớn (Big Data).",
    '002': "Đường nét lòng bàn tay cân đối. Dự báo học kỳ này bạn sẽ quản lý thời gian cực tốt, không lo ngập deadline.",
    '003': "Một đường chỉ tay chạy thẳng tắp! Bạn là người có quyết tâm cao, một khi đã tập trung học là không gì cản nổi.",
    '004': "Cấu trúc chỉ tay hình chữ M. Đây là dấu hiệu của những chuyên gia phân tích vi mô xuất sắc trong tương lai.",
    '005': "Các đường nét đan xen linh hoạt. Bạn có khả năng thích ứng cao, làm việc nhóm hay làm độc lập đều cân được hết.",
    '006': "Đường trí đạo (Head line) rõ nét. Bạn hợp với việc tự nghiên cứu giáo trình sâu xa hơn là học vẹt, học tủ.",
    '007': "Chỉ tay cho thấy bạn có nguồn năng lượng dồi dào. Rất thích hợp để duy trì một lịch trình tập gym hoặc thể thao đều đặn.",
    '008': "Đường nét thanh thoát. Bạn có xu hướng giải quyết các bài toán phức tạp bằng những cách tối giản và thông minh nhất.",
    '009': "Chỉ tay cho thấy bạn là người thực tế. Bạn luôn thích hành động ngoài đời thực để tạo ra kết quả hơn là ngồi suy nghĩ mơ mộng.",
    '010': "Dấu hiệu của một người có độ tập trung cao. Nếu bạn bật các ứng dụng chặn mạng xã hội để học, hiệu suất sẽ tăng gấp 3 lần.",
    '011': "Các đường nét tập trung ở vùng trung tâm. Bạn có tiềm năng quản trị và tối ưu hóa tài nguyên rất tốt (như quản lý base game vậy).",
    '012': "Đường chỉ tay sâu và rõ. Học kỳ này dự báo bạn sẽ gặp được những người bạn đồng hành (teammates) cực kỳ gánh tạ.",
    '013': "Chỉ tay hướng ngoại. Bạn rất có duyên với các hoạt động thuyết trình, làm việc với dữ liệu khách hàng hoặc khảo sát thị trường.",
    '014': "Đường nét cho thấy sự kiên trì ngầm. Dù lúc học lúc chơi nhưng đến giai đoạn nước rút, bạn cày cuốc không ai bằng.",
    '015': "Dấu hiệu của tư duy phản biện. Bạn không dễ dàng chấp nhận các công thức có sẵn mà luôn hỏi 'Tại sao nó lại đúng?'.",
    '016': "Đường chỉ tay mềm mại. Bạn là người có gu thẩm mỹ tốt, rất hợp với việc thiết kế giao diện (UI) hoặc trực quan hóa dữ liệu (Visualization).",
    '017': "Cấu trúc chỉ tay cân bằng giữa lý thuyết và thực hành. Bạn biết cách biến những kiến thức khô khan thành công cụ ứng dụng được.",
    '018': "Dự báo bạn sắp tìm ra một hướng đi, một dự án cá nhân thực tế khiến bạn vô cùng hứng thú trong thời gian tới.",
    '019': "Chỉ tay của người có trực giác tốt. Trong các bài kiểm tra trắc nghiệm, những câu bạn phân vân thường có tỉ lệ đúng rất cao.",
    '020': "Đường nét cho thấy sự ngăn nắp trong tư duy. Bạn hợp với việc thiết kế cấu trúc database hoặc hệ thống thông tin.",
    '021': "Bạn có khả năng tự học rất mạnh mẽ. Những kiến thức tự cày cuốc bên ngoài sẽ giúp ích lớn cho sự nghiệp của bạn.",
    '022': "Chỉ tay của một người có tính kiên nhẫn cao với các con số. Việc debug code hay làm sạch data không làm khó được bạn.",
    '023': "Dấu hiệu của sự bứt phá. Chỉ cần bạn vượt qua được chương đầu tiên của những môn khó, các chương sau sẽ xuôi chèo mát mái.",
    '024': "Đường nét cho thấy bạn rất có duyên với các tài liệu tiếng Anh chuyên ngành. Đọc hiểu tài liệu nước ngoài là thế mạnh của bạn.",
    '025': "Chỉ tay của người thích sự rõ ràng, minh bạch. Bạn làm việc gì cũng cần có quy trình và kế hoạch cụ thể.",
    '026': "Đường nét chỉ tay cho thấy bạn có khả năng giữ bình tĩnh rất tốt trước áp lực cao (như áp lực mùa thi cử).",
    '027': "Dấu hiệu của sự sáng tạo ngầm. Bạn thường có những giải pháp độc lạ cho những bài toán mà người khác bỏ cuộc.",
    '028': "Chỉ tay cho thấy bạn là người có trách nhiệm cao. Khi được giao một task trong nhóm, bạn sẽ làm đến nơi đến chốn.",
    '029': "Bạn hợp với những môi trường yên tĩnh như thư viện trường để phát huy tối đa công suất học tập của mình.",
    '030': "Đường nét cho thấy bạn là người không thích rập khuôn. Bạn luôn tìm cách cải tiến những quy trình cũ kỹ.",
    '031': "Chỉ tay dự báo bạn có khả năng kết nối dữ liệu từ nhiều nguồn khác nhau để tìm ra bản chất vấn đề.",
    '032': "Dấu hiệu của một người có tư duy chiến lược tốt, hợp với việc lập kế hoạch dài hạn cho các dự án.",
    '033': "Đường chỉ tay rõ ràng, ít nét thừa. Bạn thuộc tuýp người nói được làm được, tư duy thiên về hành động thực tế.",
    '034': "Bạn có khả năng lọc bỏ những thông tin nhiễu để tập trung vào những giá trị cốt lõi nhất của bài toán.",
    '035': "Chỉ tay cho thấy bạn có duyên với các thuật toán tối ưu hóa. Càng những bài toán hóc búa càng kích thích bạn tư duy.",
    '036': "Đường nét cho thấy sự bền bỉ. Điểm số của bạn có thể không bùng nổ ngay từ đầu nhưng sẽ tăng trưởng rất ổn định.",
    '037': "Bạn có khả năng nhìn ra các quy luật (patterns) ẩn sâu trong các tập dữ liệu phức tạp.",
    '038': "Chỉ tay của người có đầu óc logic và thực chứng. Bạn chỉ tin vào những gì có số liệu chứng minh rõ ràng.",
    '039': "Dấu hiệu cho thấy bạn rất nhạy bén với các xu hướng công nghệ mới. Việc cập nhật công cụ AI là lợi thế của bạn.",
    '040': "Đường nét tổng hòa tốt. Bạn có khả năng cân bằng tuyệt vời giữa việc học tập phát triển sự nghiệp và tận hưởng cuộc sống.",
    '041': "Chỉ tay cho thấy bạn là người có khả năng lãnh đạo tốt. Bạn biết cách truyền cảm hứng và dẫn dắt người khác hướng tới mục tiêu chung."
}

def build_model(num_classes: int, image_size: tuple[int, int]) -> tf.keras.Model:
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(image_size[0], image_size[1], 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax'),
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy'],
    )
    return model

def make_generators(data_root: Path, image_size: tuple[int, int], batch_size: int):
    train_dir = data_root / 'train'
    test_dir = data_root / 'test'

    if not train_dir.exists():
        raise FileNotFoundError(f"Train directory not found: {train_dir}")
    if not test_dir.exists():
        raise FileNotFoundError(f"Test directory not found: {test_dir}")

    # Tích hợp các thông số augmentation mới của bạn và giữ lại validation_split
    train_val_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.1
    )

    test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    train_generator = train_val_datagen.flow_from_directory(
        train_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True,
    )

    validation_generator = train_val_datagen.flow_from_directory(
        train_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False,
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False,
    )

    return train_generator, validation_generator, test_generator

def print_sample_predictions(model: tf.keras.Model, generator, index_to_class: dict, limit: int = 5):
    batch_x, batch_y = next(generator)
    predictions = model.predict(batch_x, verbose=0)

    print('\nSample predictions:')
    for idx in range(min(limit, len(batch_x))):
        predicted_index = int(np.argmax(predictions[idx]))
        true_index = int(np.argmax(batch_y[idx]))
        predicted_label = index_to_class[predicted_index]
        true_label = index_to_class[true_index]
        print(f"- image {idx + 1}: true={true_label}, predicted={predicted_label}")

        # Gọi thông điệp từ fortune_telling_db
        message = fortune_telling_db.get(predicted_label, 'Không có thông điệp cho nhãn này.')
        print(f"  {message}\n")

# ==========================================
# HYPERPARAMETERS & CONFIGURATION
# Thay thế argparse bằng các biến cấu hình trực tiếp
# ==========================================
DATA_ROOT = '/content/drive/MyDrive/archive'  # Thay đổi nếu thư mục giải nén của bạn khác
MODEL_PATH = 'palmistry_cnn.keras'
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 15
RETRAIN = True  # Đổi thành False nếu đã có file model và chỉ muốn load lại

data_root = Path(DATA_ROOT)
model_path = Path(MODEL_PATH)

# Khởi tạo generators
train_generator, validation_generator, test_generator = make_generators(data_root, IMAGE_SIZE, BATCH_SIZE)
num_classes = len(train_generator.class_indices)
index_to_class = {index: label for label, index in train_generator.class_indices.items()}

# Logic Train / Load model
if model_path.exists() and not RETRAIN:
    print(f'Loading existing model from {model_path}...')
    model = tf.keras.models.load_model(model_path)
else:
    print('Building and training new model...')
    model = build_model(num_classes, IMAGE_SIZE)
    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=4,
            restore_best_weights=True,
        )
    ]

    validation_steps = max(1, len(validation_generator))

    # Bắt đầu quá trình học (fitting)
    model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        validation_steps=validation_steps,
        callbacks=callbacks,
    )

    model.save(model_path)
    print(f'Saved model to {model_path}')

# Đánh giá trên tập test
print("\nEvaluating on test set...")
test_generator.reset()
test_loss, test_accuracy = model.evaluate(test_generator, verbose=1)
print(f'Test loss: {test_loss:.4f}')
print(f'Test accuracy: {test_accuracy:.4f}')

# In dự đoán mẫu kèm lời bói
test_generator.reset()
print_sample_predictions(model, test_generator, index_to_class)