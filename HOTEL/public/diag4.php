<?php
$f = 'D:/桌面/国际/JD-main/HOTEL/public/index.html';
$html = file_get_contents($f);

// 提取 script 内容
if (preg_match('/<script>([\s\S]*?)<\/script>/s', $html, $m)) {
    $js = $m[1];
    // 找到 PMS 相关区域
    $pmsStart = strpos($js, 'PMS AI');
    
    if ($pmsStart !== false) {
        // 提取PMS区域前后各100字符
        $start = max(0, $pmsStart - 80);
        $len = 300;
        echo "=== PMS区域 (pos $pmsStart) ===\n";
        echo substr($js, $start, $len) . "\n\n";
        
        // 检查是否有特殊字符
        $chunk = substr($js, $pmsStart, 5000);
        for ($i = 0; $i < strlen($chunk); $i++) {
            $c = ord($chunk[$i]);
            if ($c > 127 && $c < 192) {
                printf("非ASCII字符 at offset %d: 0x%02x (%s)\n", $i+$pmsStart+1, $c, json_encode($chunk[$i]));
            }
        }
    }
}
