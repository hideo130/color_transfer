# color_transfer

Color Transfer Between images[^1]の実装をしました．
詳しくは[qiita][2]にまとめました．

# 実行結果
![入力画像](readme_images/fig1.png)
![参照画像](readme_images/fig2.png)
![実験結果](readme_images/source=fig1target=fig2.png)
![論文中の実験結果](readme_images/reference2.png)
左から順に入力画像，参照画像，自分の実験結果，論文中の実験結果です．右から2番目の実験結果の色がおかしくなりました．
macで論文中の画像をスクリーンショットする事で，入力画像と参照画像を獲得しました．

# todo
クラスタリングして各クラスタで異なる色の変換を行えるようにする．

[^1]:https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf

[2]:https://qiita.com/wkiino/items/f4a8f340016951107646


