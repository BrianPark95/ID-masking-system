UI 파일
: pyqt5로 만들어진 ui로 실행시킨  후 이미지를 불러오면 IDcard의 정보가 읽어지고 원하는 이름, 주민등록번호, 주소, 얼굴이 블러링 되는 ui이다.

Capture파일
: capture파일을 실행한 곳에 웹캠으로 찍은 사진이 저장되며, 파일명의 경우 코드에서 pixmap.save의 파일명을 바꿔주면 쉽게 파일명을 바꿀 수 있다.
  capture파일을 이용해 idcard를 저장하고 저장한 idcard를 ui파일을 사용해 내용을 추출하는 원리이다.