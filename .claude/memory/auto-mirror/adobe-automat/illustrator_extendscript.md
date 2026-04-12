# Illustrator ExtendScript — detailní reference

## Extrakce textů z .ai souboru

```javascript
var doc = app.activeDocument;
var results = [];
function getLayerTexts(layer) {
    var layerData = { layerName: layer.name, layerId: layer.zOrderPosition, texts: [] };
    for (var i = 0; i < layer.textFrames.length; i++) {
        var tf = layer.textFrames[i];
        var fontSize = 0;
        try { fontSize = tf.textRange.characterAttributes.size; } catch(e) {}
        layerData.texts.push({
            index: i, contents: tf.contents,
            position: [Math.round(tf.position[0]*100)/100, Math.round(tf.position[1]*100)/100],
            width: Math.round(tf.width*100)/100, height: Math.round(tf.height*100)/100,
            kind: tf.kind.toString(), fontSize: fontSize
        });
    }
    return layerData;
}
var mainLayer = doc.layers[0];
for (var s = 0; s < mainLayer.layers.length; s++) {
    var sub = mainLayer.layers[s];
    if (sub.textFrames.length > 0) results.push(getLayerTexts(sub));
}
return JSON.stringify(results);
```

## Zápis překladů (batch pattern)

```javascript
var doc = app.activeDocument;
var mainLayer = doc.layers[0];
var changed = 0; var errors = [];
var translations = [["original", "czech"], ...];

for (var s = 0; s < mainLayer.layers.length; s++) {
    var sub = mainLayer.layers[s];
    if (sub.name === "LAYER_NAME") {
        for (var i = 0; i < sub.textFrames.length; i++) {
            var tf = sub.textFrames[i];
            for (var t = 0; t < translations.length; t++) {
                if (tf.contents === translations[t][0]) {
                    try { tf.contents = translations[t][1]; changed++; }
                    catch(e) { errors.push({index:i, error:e.toString()}); }
                    break;
                }
            }
        }
        break;
    }
}
return JSON.stringify({changed: changed, errors: errors});
```

## Export PNG přes ExtendScript

```javascript
var doc = app.activeDocument;
var destFile = new File("C:/Users/stock/.../output.png");
var opts = new ExportOptionsPNG24();
opts.horizontalScale = 200;
opts.verticalScale = 200;
opts.artBoardClipping = true;
opts.antiAliasing = true;
opts.transparency = false;
doc.exportFile(destFile, ExportType.PNG24, opts);
return JSON.stringify({exported: true, path: destFile.fsName});
```

## Důležité poznámky

- `\r` v `.contents` = zalomení řádku v textovém rámci
- `tf.kind.toString()` vrací typ (PointText, AreaText...)
- `tf.textRange.characterAttributes.size` — font size v pt
- Batch limit: ~30 překladů na jedno volání ExtendScript
- JSON.stringify POVINNÝ pro návratové hodnoty (json-polyfill.jsx)
