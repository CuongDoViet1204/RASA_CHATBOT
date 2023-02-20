# RASA_CHATBOT
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
