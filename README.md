# CHATBOT DỰ ĐOÁN BỆNH TỪ TRIỆU CHỨNG - RASA_CHATBOT
Bài tập lớn học phần Nhập môn Trí tuệ nhân tạo (Cô Lê Thanh Hương).

Xây dựng chatbot đự đoán bệnh từ triệu chứng của người dùng.

***Thành viên nhóm:**
- Đỗ Việt Cường 20200073
- Nguyễn Tấn Dũng 20200103
- Nguyễn Văn Khánh 20200322
- Trần Quốc Nam Phi 20200459
- Trần Quang Tiến 20200540

**1. Framework và thuật toán:**
- Ngôn ngữ: Python.
- Framework: RASA (NLU + Core + X + Intent). Tham khảo: https://rasa.com/docs/rasa/
- Machine Learning model: RandomForest (rừng ngẫu nhiên). Training trên tập đào tạo gồm 4920 mẫu thử với 132 triệu chứng và 41 bệnh.
- Dataset: https://www.kaggle.com/datasets/rabisingh/symptom-checker .
  
**2. Cài đặt và thực thi:**

Cài đặt môi trường ảo:
  - python -m venv venv
  - venv\Scripts\activate

Để chạy được chương trình, máy cần install một số thư viện sau:
  - numpy: pip install numpy  
  - pandas: pip install pandas
  - sklearn: pip install -U scikit-learn
  - matplotlib: pip install matplotlib
  - googletrans: pip install googletrans==4.0rc1
  - frameword Rasa: pip install rasa
  
Mở terminal chạy file setup:
  python setup.py install
  
Để chạy, mở 2 terminal chạy song song, cd đến folder chatbotDemo:
  - 1 terminal chạy rasa run actions
  - khởi tạo xong server chạy rasa shell ở terminal còn lại
