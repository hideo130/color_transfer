# color_transfer

https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf
を実装を試みたが，上手くいかず原因も分かりませんでした．
論文に乗っているRGBからXYZ色空間への変換行列は何を元にして得られたのか不明だったため，sRGBからXYZ色空間への変換式を利用しました．
<!-- 具体的な変換手順は例えば教科書に乗っています．
https://www.springer.com/jp/book/9781447166832 -->
論文に乗っているlab色空間での変換式(10),(11)はcolor_transfer内に記述してあります．

# 実行結果
![入力画像](readme_images/fig1.png)

自分の実験結果は次のようになりました．


# 確認したいこと
式(11)でl’を求めた後に加算するのは参照画像の平均であってますか？
