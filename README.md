# MIS_HW4
#檔案說明

書面報告.pdf:HW4書面報告

HW3_DEMO.pdf:HW3課堂DEMO投影片

/MIS_HW3:作業3

/MIS_HW4:作業4



#/MIS_HW4操作流程:
1.執行offlineDataGenerator_avgRGB.py & offlineDataGenerator_avgHSV.py & offlineDataGenerator_ColorLayout.py，
產生csv檔的offlineData（檔案中已有data存於"offlineData"資料夾內，因此可略過此步）
2.執行Mosaic_GUI.py，開啟GUI介面，選擇檔案、模式、距離計算公式及切割大小，最後按"START"執行。
3.圖片會顯示於右側，並儲存為一個product.jpg檔。

#/MIS_HW3操作流程:
1.執行Q2.py，產生csv檔的offlineData，存於"offline"資料夾內。（資料夾內已有，可略過）
2.執行SIFT_Converter.py產生各圖片的sift檔，存於"offline/sift"資料夾內。（資料夾內已有，可略過）
3.執行Q3.py(需存在sift檔)，產生csv檔的offlineData，存於"offline"資料夾內。（資料夾內已有，可略過）
4.執行Search_Gui.py，開啟GUI介面，選擇檔案、模式，最後按下"SEARCH"搜尋。
5.10張圖片會顯示於下側，上排從左到右為計算距離最相近的1~5張，下排左到右是6~10張。
