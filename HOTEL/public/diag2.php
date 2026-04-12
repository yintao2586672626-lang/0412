<?php
// 提取 <script setup> 区域并做基础JS语法检查
$html = file_get_contents('D:/桌面/国际/JD-main/HOTEL/public/index.html');
preg_match('/<script[^>]*>([\s\S]*?)<\/script>/', $html, $matches);
if (!$matches) {
    echo "No script tag found\n";
    exit;
}
$js = $matches[1];
// 写入临时文件
file_put_contents('D:/桌面/国际/JD-main/HOTEL/public/check_js.js', $js);
echo "Extracted JS length: " . strlen($js) . " chars\n";
// 基本括号平衡
$opens = substr_count($js, '{');
$closes = substr_count($js, '}');
$parensO = substr_count($js, '(');
$parensC = substr_count($js, ')');
$bracketO = substr_count($js, '[');
$bracketC = substr_count($js, ']');
echo "Braces: {$opens} open, {$closes} close (diff:" . ($opens-$closes) . ")\n";
echo "Parens: {$parensO} open, {$parensC} close (diff:" . ($parensO-$parensC) . ")\n";
echo "Brackets: {$bracketO} open, {$bracketC} close (diff:" . ($bracketO-$bracketC) . ")\n";

// 检查最近修改区域是否有明显问题
$lines = explode("\n", $js);
$total = count($lines);
echo "\nTotal JS lines: {$total}\n";
echo "\n--- Last 30 lines of JS ---\n";
for ($i = max(0, $total - 35); $i < $total; $i++) {
    printf("%04d: %s\n", $i + 1, $lines[$i]);
}
