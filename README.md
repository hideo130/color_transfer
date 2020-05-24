# color_transfer

Color Transfer Between images[^1]の実装をしました．
入力画像の色味を参照画像の色味に近づける画像処理アルゴリズムです．

実行方法
```
python3 color_transfer. py source_img_path target_img_path save_dir/
```

アルゴリズムの詳細は[qiita][2]に書きました．

# 実行結果
|入力画像|参照画像|実行結果|入力画像と参照画像を逆に|論文中の結果|
|---|---|---|---|---|
|![参照画像](readme_images/fig2.png)|![入力画像](readme_images/fig1.png)|![逆に](readme_images/source=fig2target=fig1.png)|![入力画像と参照画像を逆に](readme_images/source=fig1target=fig2.png)|![論文中の実験結果](readme_images/reference2.png)|

左から順に入力画像，参照画像，自分の実験結果，入力画像と参照画像を逆にした結果，論文中に乗っていた実験結果です． 
入力画像の色が参照画像の色に近づきます．

[1]:https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf

[2]:https://qiita.com/wkiino/items/f4a8f340016951107646


