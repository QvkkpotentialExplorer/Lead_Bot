FROM python:3.11

# ������� ���������� /lb � ������������� � ��� �������
WORKDIR /lb

# �������� ����� ������� � ������� ���������� ����������
COPY . .

# ������������� ����������� �� requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ��������� ����
CMD ["python", "bot.py"]
