#!/usr/bin/env python3
"""
Tailwind CSS 精简工具 - 根据实际使用的类名生成最小化 CSS
"""

import re
import os

# 读取提取的类名
CLASSES_FILE = os.path.join(os.path.dirname(__file__), 'tailwind-classes.txt')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'tailwind-custom.css')

with open(CLASSES_FILE, 'r', encoding='utf-8') as f:
    raw_classes = [line.strip() for line in f if line.strip()]

# 清理类名（去除尾部引号、过滤非 Tailwind 类）
clean_classes = set()
for c in raw_classes:
    c_clean = c.rstrip("'").rstrip('"')
    # 只保留有效的 Tailwind 类名格式
    if re.match(r'^[a-z]([\w\-/\.:\[\]\d]+)?$', c_clean) and len(c_clean) < 50 and not c_clean.startswith('//'):
        clean_classes.add(c_clean)

print(f"Clean Tailwind classes count: {len(clean_classes)}")

# ============================================
# Tailwind CSS 规则映射表（只包含项目用到的）
# ============================================

def generate_css(classes):
    css_parts = []
    css_parts.append("/* tailwind-custom.css - Auto-generated optimized Tailwind */")
    css_parts.append(f"/* Generated: {len(classes)} unique classes extracted from project */")
    css_parts.append("")
    
    # CSS Reset / Base
    css_parts.append("""/* ===== Base Reset ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { line-height: 1.5; -webkit-text-size-adjust: 100%; tab-size: 4; font-family: ui-sans-serif, system-ui, sans-serif; }
body { min-height: 100%; line-height: inherit; }
""")

    # Layout
    css_parts.append("""/* ===== Display ===== */""")
    display_map = {
        'block': 'display: block',
        'inline-block': 'display: inline-block',
        'inline-flex': 'display: inline-flex',
        'inline': 'display: inline',
        'flex': 'display: flex',
        'grid': 'display: grid',
        'hidden': 'display: none',
        'table': 'display: table',
    }
    for cls in [c for c in classes if c in display_map]:
        css_parts.append(f".{cls} {{ {display_map[cls]}; }}")

    # Position
    css_parts.append("\n/* ===== Position ===== */")
    position_map = {
        'static': 'position: static', 'relative': 'position: relative', 'absolute': 'position: absolute',
        'fixed': 'position: fixed', 'sticky': 'position: sticky',
    }
    for cls in [c for c in classes if c in position_map]:
        css_parts.append(f".{cls} {{ {position_map[cls]}; }}")

    inset_classes = [c for c in classes if c == 'inset-0']
    if inset_classes:
        css_parts.append(".inset-0 { top: 0; right: 0; bottom: 0; left: 0; }")

    # Top/Right/Bottom/Left
    trbl_map = {
        'top-0': ('top', '0'), 'top-0.5': ('top', '2px'), 'top-3': ('top', '12px'),
        'top-4': ('top', '16px'), 'top-1/2': ('top', '50%'),
        'bottom-0': ('bottom', '0'), 'bottom-12': ('bottom', '48px'),
        'left-0': ('left', '0'), 'left-0.5': ('left', '2px'), 'left-3': ('left', '12px'),
        'right-0': ('right', '0'), 'right-3': ('right', '12px'), 'right-4': ('right', '16px'), 'right-6': ('right', '24px'),
    }
    css_parts.append("\n/* ===== Top/Right/Bottom/Left ===== */")
    for cls in [c for c in classes if c in trbl_map]:
        prop, val = trbl_map[cls]
        css_parts.append(f".{cls} {{ {prop}: {val}; }}")

    # Flexbox
    css_parts.append("\n/* ===== Flexbox ===== */")
    flex_map = {
        'flex-1': 'flex: 1 1 0%', 'flex-shrink-0': 'flex-shrink: 0',
        'flex-col': 'flex-direction: column', 'flex-wrap': 'flex-wrap', 'flex-row': 'flex-direction: row',
    }
    for cls in [c for c in classes if c in flex_map]:
        css_parts.append(f".{cls} {{ {flex_map[cls]}; }}")

    items_map = {'items-center': 'align-items: center', 'items-start': 'align-items: flex-start', 'items-end': 'align-items: flex-end'}
    for cls in [c for c in classes if c in items_map]:
        css_parts.append(f".{cls} {{ {items_map[cls]}; }}")

    justify_map = {'justify-between': 'justify-content: space-between', 'justify-center': 'justify-content: center', 'justify-end': 'justify-content: flex-end'}
    for cls in [c for c in classes if c in justify_map]:
        css_parts.append(f".{cls} {{ {justify_map[cls]}; }}")

    self_map = {'self-center': 'align-self: center'}
    for cls in [c for c in classes if c in self_map]:
        css_parts.append(f".{cls} {{ {self_map[cls]}; }}")

    # Grid
    css_parts.append("\n/* ===== Grid ===== */")
    grid_col_map = {}
    for c in classes:
        m = re.match(r'grid-cols-(\d)', c)
        if m: grid_col_map[c] = f'grid-template-columns: repeat({m.group(1)}, minmax(0, 1fr))'
    col_span_map = {}
    for c in classes:
        m = re.match(r'col-span-(\d)', c)
        if m: col_span_map[c] = f'grid-column: span {m.group(1)} / span {m.group(1)}'
    for cls in sorted(list(set(list(grid_col_map.keys()) + list(col_span_map.keys())))):
        if cls in grid_col_map: css_parts.append(f".{cls} {{ {grid_col_map[cls]}; }}")
        if cls in col_span_map: css_parts.append(f".{cls} {{ {col_span_map[cls]}; }}")

    # Width & Height
    css_parts.append("\n/* ===== Sizing ===== */")
    size_map = {
        'w-2': 'width: 8px', 'w-3': 'width: 12px', 'w-4': 'width: 16px', 'w-5': 'width: 20px',
        'w-6': 'width: 24px', 'w-8': 'width: 32px', 'w-10': 'width: 40px', 'w-11': 'width: 44px',
        'w-12': 'width: 48px', 'w-14': 'width: 56px', 'w-16': 'width: 64px', 'w-20': 'width: 80px',
        'w-24': 'width: 96px', 'w-28': 'width: 112px', 'w-32': 'width: 128px', 'w-40': 'width: 160px',
        'w-48': 'width: 192px', 'w-56': 'width: 224px', 'w-60': 'width: 240px', 'w-64': 'width: 256px',
        'w-80': 'width: 320px', 'w-full': 'width: 100%',
        'h-2': 'height: 8px', 'h-3': 'height: 12px', 'h-4': 'height: 16px', 'h-5': 'height: 20px',
        'h-6': 'height: 24px', 'h-8': 'height: 32px', 'h-10': 'height: 40px', 'h-12': 'height: 48px',
        'h-14': 'height: 56px', 'h-20': 'height: 80px', 'h-48': 'height: 192px',
        'h-60': 'height: 240px', 'h-64': 'height: 256px', 'h-80': 'height: 320px',
        'h-full': 'height: 100%', 'h-screen': 'height: 100vh',
    }
    # Handle arbitrary values like h-[85vh], h-[1px], w-full'
    arb_h = re.compile(r'h-\[(\d+(?:\.\d+)?(?:vh|vw|px|%))\]')
    arb_w = re.compile(r'w-\[(\d+(?:\.\d+)?(?:vh|vw|px|%))\]')
    for c in classes:
        cm = arb_h.match(c)
        wm = arb_w.match(c)
        if cm: size_map[c] = f'height: {cm.group(1)}'
        if wm: size_map[c] = f'width: {wm.group(1)}'
    for cls in [c for c in classes if c in size_map]:
        css_parts.append(f".{cls} {{ {size_map[cls]}; }}")

    # Spacing (p, px, py, pt, pb, pl, pr, m, mx, my, mt, mb, ml, mr)
    css_parts.append("\n/* ===== Spacing ===== */")
    sp = {'p-1':'padding:4px','p-1.5':'padding:6px','p-2':'padding:8px','p-3':'padding:12px','p-4':'padding:16px','p-5':'padding:20px','p-6':'padding:24px','p-8':'padding:32px','p-10':'padding:40px','p-12':'padding:48px'}
    px = {'px-1':'padding-left:4px;padding-right:4px','px-1.5':'padding-left:6px;padding-right:6px','px-2':'padding-left:8px;padding-right:8px','px-2.5':'padding-left:10px;padding-right:10px','px-3':'padding-left:12px;padding-right:12px','px-4':'padding-left:16px;padding-right:16px','px-5':'padding-left:20px;padding-right:20px','px-6':'padding-left:24px;padding-right:24px'}
    py = {'py-0.5':'padding-top:2px;padding-bottom:2px','py-1':'padding-top:4px;padding-bottom:4px','py-1.5':'padding-top:6px;padding-bottom:6px','py-2':'padding-top:8px;padding-bottom:8px','py-2.5':'padding-top:10px;padding-bottom:10px','py-3':'padding-top:12px;padding-bottom:12px','py-3.5':'padding-top:14px;padding-bottom:14px','py-4':'padding-top:16px;padding-bottom:16px','py-6':'padding-top:24px;padding-bottom:24px','py-8':'padding-top:32px;padding-bottom:32px','py-12':'padding-top:48px;padding-bottom:48px','py-20':'padding-top:80px;padding-bottom:80px'}
    m = {'mt-0.5':'margin-top:2px','mt-1':'margin-top:4px','mt-2':'margin-top:8px','mt-3':'margin-top:12px','mt-4':'margin-top:16px','mt-5':'margin-top:20px','mt-6':'margin-top:24px','mt-8':'margin-top:32px','mb-1':'margin-bottom:4px','mb-1.5':'margin-bottom:6px','mb-2':'margin-bottom:8px','mb-3':'margin-bottom:12px','mb-4':'margin-bottom:16px','mb-5':'margin-bottom:20px','mb-6':'margin-bottom:24px','mb-8':'margin-bottom:32px','mb-10':'margin-bottom:40px','ml-1':'margin-left:4px','ml-2':'margin-left:8px','ml-4':'margin-left:16px','ml-6':'margin-left:24px','mr-1':'margin-right:4px','mr-1.5':'margin-right:6px','mr-2':'margin-right:8px','mr-3':'margin-right:12px'}

    spacing_all = {**sp, **px, **py, **m}
    for cls in [c for c in classes if c in spacing_all]:
        css_parts.append(f".{cls} {{ {spacing_all[cls]}; }}")

    # Gap
    gap_map = {'gap-1':'gap:4px','gap-1.5':'gap:6px','gap-2':'gap:8px','gap-3':'gap:12px','gap-4':'gap:16px','gap-5':'gap:20px','gap-6':'gap:24px'}
    for cls in [c for c in classes if c in gap_map]:
        css_parts.append(f".{cls} {{ {gap_map[cls]}; }}")

    # Space between
    space_x = {'space-x-1':'> :not([hidden])~:not([hidden]){--tw-space-x-reverse:0;margin-left:calc(4px * calc(1 - var(--tw-space-x-reverse)));margin-right:calc(4px * var(--tw-space-x-reverse))}','space-x-2':'> :not([hidden])~:not([hidden]){--tw-space-x-reverse:0;margin-left:calc(8px * calc(1 - var(--tw-space-x-reverse)));margin-right:calc(8px * var(--tw-space-x-reverse))}','space-x-3':'> :not([hidden])~:not([hidden]){--tw-space-x-reverse:0;margin-left:calc(12px * calc(1 - var(--tw-space-x-reverse)));margin-right:calc(12px * var(--tw-space-x-reverse))}','space-x-4':'> :not([hidden])~:not([hidden]){--tw-space-x-reverse:0;margin-left:calc(16px * calc(1 - var(--tw-space-x-reverse)));margin-right:calc(16px * var(--tw-space-x-reverse))}','space-x-6':'> :not([hidden])~:not([hidden]){--tw-space-x-reverse:0;margin-left:calc(24px * calc(1 - var(--tw-space-x-reverse)));margin-right:calc(24px * var(--tw-space-x-reverse))}'}
    space_y = {'space-y-1':'> :not([hidden])~:not([hidden]){--tw-space-y-reverse:0;margin-top:calc(4px * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(4px * var(--tw-space-y-reverse))}','space-y-2':'> :not([hidden])~:not([hidden]){--tw-space-y-reverse:0;margin-top:calc(8px * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(8px * var(--tw-space-y-reverse))}','space-y-3':'> :not([hidden])~:not([hidden]){--tw-space-y-reverse:0;margin-top:calc(12px * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(12px * var(--tw-space-y-reverse))}','space-y-4':'> :not([hidden])~:not([hidden]){--tw-space-y-reverse:0;margin-top:calc(16px * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(16px * var(--tw-space-y-reverse))}','space-y-5':'> :not([hidden])~:not([hidden]){--tw-space-y-reverse:0;margin-top:calc(20px * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(20px * var(--tw-space-y-reverse))}','space-y-6':'> :not([hidden])~:not([hidden]){--tw-space-y-reverse:0;margin-top:calc(24px * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(24px * var(--tw-space-y-reverse))}','space-y-8':'> :not([hidden])~:not([hidden]){--tw-space-y-reverse:0;margin-top:calc(32px * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(32px * var(--tw-space-y-reverse))}'}
    for cls in list(space_x.keys()) + list(space_y.keys()):
        if cls in classes:
            if cls in space_x: css_parts.append(f".{cls} {{{space_x[cls]}}}")
            if cls in space_y: css_parts.append(f".{cls} {{{space_y[cls]}}}")

    # Typography
    css_parts.append("\n/* ===== Typography ===== */")
    font_map = {
        'font-bold': 'font-weight: 700', 'font-semibold': 'font-weight: 600', 'font-medium': 'font-weight: 500',
        'font-light': 'font-weight: 300', 'font-normal': 'font-weight: 400', 'font-mono': 'font-family: monospace',
    }
    text_size_map = {
        'text-xs': 'font-size: 12px;line-height: 16px', 'text-sm': 'font-size: 14px;line-height: 20px',
        'text-base': 'font-size: 16px;line-height: 24px', 'text-lg': 'font-size: 18px;line-height: 28px',
        'text-xl': 'font-size: 20px;line-height: 28px', 'text-2xl': 'font-size: 24px;line-height: 32px',
        'text-3xl': 'font-size: 30px;line-height: 36px', 'text-4xl': 'font-size: 36px;line-height: 40px',
        'text-5xl': 'font-size: 48px;line-height: 1', 'text-6xl': 'font-size: 60px;line-height: 1',
    }
    text_align = {'text-left': 'text-align: left', 'text-center': 'text-align: center', 'text-right': 'text-align: right'}
    leading = {'leading-relaxed': 'line-height: 1.625'}
    tracking = {'tracking-wide': 'letter-spacing: .025em', 'tracking-wider': 'letter-spacing: .05em'}
    truncate_css = '.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }'
    whitespace_map = {'whitespace-nowrap': 'white-space: nowrap', 'whitespace-pre-wrap': 'white-space: pre-wrap'}

    for cls in [c for c in classes if c in font_map]:
        css_parts.append(f".{cls} {{ {font_map[cls]}; }}")
    for cls in [c for c in classes if c in text_size_map]:
        css_parts.append(f".{cls} {{ {text_size_map[cls]}; }}")
    for cls in [c for c in classes if c in text_align]:
        css_parts.append(f".{cls} {{ {text_align[cls]}; }}")
    for cls in [c for c in classes if c in leading]:
        css_parts.append(f".{cls} {{ {leading[cls]}; }}")
    for cls in [c for c in classes if c in tracking]:
        css_parts.append(f".{cls} {{ {tracking[cls]}; }}")
    if 'truncate' in classes: css_parts.append(truncate_css)
    for cls in [c for c in classes if c in whitespace_map]:
        css_parts.append(f".{cls} {{ {whitespace_map[cls]}; }}")

    # Arbitrary text sizes
    for c in classes:
        tm = re.match(r'text-\[(\d+px)\]', c)
        if tm: css_parts.append(f".{{c}} {{ font-size: {tm.group(1)}; }}")

    # Colors - Text colors
    css_parts.append("\n/* ===== Text Colors ===== */")
    text_colors = {}
    color_values = {
        'white': '#fff', 'black': '#000', 
        'gray-300': '#d1d5db', 'gray-400': '#9ca3af', 'gray-500': '#6b7280',
        'gray-600': '#4b5563', 'gray-700': '#374151', 'gray-800': '#1f2937',
        'gray-900': '#111827', 'slate-400': '#94a3b8', 'slate-500': '#64748b',
        'blue-500': '#3b82f6', 'blue-600': '#2563eb', 'blue-700': '#1d4ed8',
        'blue-800': '#1e40af', 'blue-300': '#93c5fd', 'blue-100': '#dbeafe',
        'green-400': '#4ade80', 'green-500': '#22c55e', 'green-600': '#16a34a',
        'green-700': '#15803d', 'green-800': '#166534', 'green-100': '#dcfce7',
        'red-400': '#f87171', 'red-500': '#ef4444', 'red-600': '#dc2626',
        'red-700': '#b91c1c', 'red-800': '#991b1b', 'red-100': '#fee2e2',
        'red-900': '#7f1d1d',
        'amber-500': '#f59e0b', 'amber-600': '#d97706', 'amber-700': '#b45309',
        'orange-500': '#f97316', 'orange-600': '#ea580c', 'orange-700': '#c2410c',
        'orange-800': '#9a3412', 'orange-100': '#ffedd5',
        'indigo-400': '#818cf8', 'indigo-500': '#6366f1', 'indigo-600': '#4f46e5',
        'indigo-700': '#4338ca', 'indigo-800': '#3730a3', 'indigo-100': '#e0e7ff',
        'purple-100': '#f3e8ff', 'purple-300': '#d8b4fe', 'purple-400': '#c084fc',
        'purple-600': '#9333ea', 'purple-700': '#7e22ce', 'purple-800': '#6b21a8',
        'pink-500': '#ec4899', 'pink-600': '#db2777', 'pink-700': '#be185d',
        'pink-800': '#9d174d',
        'teal-500': '#14b8a6', 'teal-600': '#0d9488', 'teal-800': '#115e59',
        'cyan-500': '#06b6d4', 'cyan-600': '#0891b2', 'cyan-700': '#0e7490',
        'emerald-300': '#86efac',
        'yellow-500': '#eab308', 'yellow-600': '#ca8a04', 'yellow-700': '#a16207',
        'yellow-800': '#854d0e', 'yellow-900': '#713f12',
    }
    for c in classes:
        if c.startswith('text-') and not c.startswith('text-xs') and not c.startswith('text-sm') and not c.startswith('text-base') and not c.startswith('text-lg') and not c.startswith('text-xl') and not c.startswith('text-2xl') and not c.startswith('text-3xl') and not c.startswith('text-4xl') and not c.startswith('text-5xl') and not c.startswith('text-6xl'):
            # Parse text-color variants
            base_color = c.replace('text-', '')
            opacity_suffix = ''
            if '/' in base_color:
                parts = base_color.split('/')
                base_color = parts[0]
                op_val = parts[1]
                if opacity_suffix and '/' not in opacity_suffix and all(c.isdigit() for c in opacity_suffix): opacity_suffix = '/' + op_val
            
            full_key = base_color
            if full_key in color_values:
                val = color_values[full_key]
                # Handle opacity
                if opacity_suffix:
                    op_num = int(opacity_suffix.lstrip('/')) if opacity_suffix and opacity_suffix.lstrip('/').isdigit() else 50
                    alpha_hex = format(round(op_num * 255 / 100), '02x')
                    css_parts.append(f".{c} {{ color: {val}{alpha_hex}; }}")
                else:
                    css_parts.append(f".{c} {{ color: {val}; }}")

    # Background colors
    css_parts.append("\n/* ===== Background Colors ===== */")
    bg_extra = {
        'bg-transparent': 'background-color: transparent', 'bg-white': 'background-color: #ffffff',
        'bg-black': 'background-color: #000000', 'bg-gray-50': 'background-color: #f9fafb',
        'bg-gray-100': 'background-color: #f3f4f6', 'bg-gray-200': 'background-color: #e5e7eb',
        'bg-gray-300': 'background-color: #d1d5db', 'bg-gray-500': 'background-color: #6b7280',
        'bg-gray-900': 'background-color: #111827',
    }
    bg_opacities = {
        'bg-white/10': 'rgba(255,255,255,0.1)', 'bg-white/20': 'rgba(255,255,255,0.2)',
        'bg-white/60': 'rgba(255,255,255,0.6)',
        'bg-black/5': 'rgba(0,0,0,0.05)', 'bg-black/10': 'rgba(0,0,0,0.1)',
        'bg-black/20': 'rgba(0,0,0,0.2)',
    }

    for cls in [c for c in classes if c in bg_extra]:
        css_parts.append(f".{cls} {{ {bg_extra[cls]}; }}")
    for cls in [c for c in classes if c in bg_opacities]:
        css_parts.append(f".{cls} {{ background-color: {bg_opacities[cls]}; }}")

    for c in classes:
        if c.startswith('bg-') and c not in bg_extra and c not in bg_opacities:
            base_color = c.replace('bg-', '')
            if '/' in base_color:
                parts = base_color.split('/')
                bc = parts[0]; op_str = parts[1]
                if bc in color_values and op_str.endswith('0'):
                    try:
                        alpha_hex = format(round(int(op_str[:-1]) * 255 / 100), '02x')
                        css_parts.append(f".{c} {{ background-color: {color_values[bc]}{alpha_hex}; }}")
                    except: pass
            elif base_color in color_values:
                css_parts.append(f".{c} {{ background-color: {color_values[base_color]}; }}")

    # Gradient
    gradient_map = {'bg-gradient-to-r': 'background-image: linear-gradient(to right, var(--tw-gradient-stops))', 'bg-gradient-to-br': 'background-image: linear-gradient(to bottom right, var(--tw-gradient-stops))'}
    via_colors = {'via-indigo-500/20': '--tw-gradient-to: rgb(99 102 241 / 0.2); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to); --tw-gradient-via: rgb(99 102 241 / 0.2)', 'via-indigo-600': '--tw-gradient-to: rgb(79 70 229); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to); --tw-gradient-via: rgb(79 70 229)', 'via-orange-500': '--tw-gradient-to: rgb(249 115 22); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to); --tw-gradient-via: rgb(249 115 22)', 'via-pink-600': '--tw-gradient-to: rgb(219 39 119); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to); --tw-gradient-via: rgb(219 39 119)', 'via-purple-500/20': '--tw-gradient-to: rgb(168 85 247 / 0.2); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-via), var(--tw-gradient-to); --tw-gradient-via: rgb(168 85 247 / 0.2)'}
    for cls in [c for c in classes if c in gradient_map]:
        css_parts.append(f".{cls} {{ {gradient_map[cls]}; }}")
    for cls in [c for c in classes if c in via_colors]:
        css_parts.append(f".{cls} {{ {via_colors[cls]}; }}")

    # Border
    css_parts.append("\n/* ===== Borders ===== */")
    border_widths = {'border': 'border-width: 1px', 'border-2': 'border-width: 2px', 'border-b': 'border-bottom-width: 1px', 'border-b-2': 'border-bottom-width: 2px', 'border-t': 'border-top-width: 1px', 'border-l-2': 'border-left-width: 2px', 'border-l-4': 'border-left-width: 4px', 'border-none': 'border-style: none'}
    border_radiuses = {'rounded': 'border-radius: 0.25rem', 'rounded-sm': 'border-radius: 0.125rem', 'rounded-md': 'border-radius: 0.375rem', 'rounded-lg': 'border-radius: 0.5rem', 'rounded-xl': 'border-radius: 0.75rem', 'rounded-2xl': 'border-radius: 1rem', 'rounded-full': 'border-radius: 9999px', 'rounded-t': 'border-top-left-radius: 0.25rem;border-top-right-radius: 0.25rem', 'rounded-t-lg': 'border-top-left-radius: 0.5rem;border-top-right-radius: 0.5rem', 'rounded-bl-full': 'border-bottom-left-radius: 9999px', 'rounded-r-lg': 'border-bottom-right-radius: 0.5rem;border-top-right-radius: 0.5rem'}
    
    for cls in [c for c in classes if c in border_widths]:
        css_parts.append(f".{cls} {{ {border_widths[cls]}; }}")
    for cls in [c for c in classes if c in border_radiuses]:
        css_parts.append(f".{cls} {{ {border_radiuses[cls]}; }}")

    # Border colors
    for c in classes:
        if c.startswith('border-') and c not in border_widths and c not in border_radiuses:
            bc = c.replace('border-', '')
            if '/' in bc:
                parts = bc.split('/'); bcn = parts[0]; opv = parts[1]
                if bcn in color_values:
                    ah = format(round(int(opv) * 255 / 100), '02x')
                    css_parts.append(f".{{c}} {{ border-color: {color_values[bcn]}{{ah}}; }}")
            elif bc in color_values:
                css_parts.append(f".{c} {{ border-color: {color_values[bc]}; }}")

    # Shadows
    css_parts.append("\n/* ===== Shadows ===== */")
    shadow_map = {
        'shadow-sm': 'box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'shadow-md': 'box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'shadow-lg': 'box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        'shadow-xl': 'box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        'shadow-2xl': 'box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25)',
        'drop-shadow-lg': 'filter: drop-shadow(0 10px 8px rgb(0 0 0 / 0.04)) drop-shadow(0 4px 3px rgb(0 0 0 / 0.1))',
    }
    for cls in [c for c in classes if c in shadow_map]:
        css_parts.append(f".{cls} {{ {shadow_map[cls]}; }}")

    # Opacity
    css_parts.append("\n/* ===== Opacity ===== */")
    op_map = {'opacity-10': 'opacity: 0.1', 'opacity-30': 'opacity: 0.3', 'opacity-50': 'opacity: 0.5', 'opacity-70': 'opacity: 0.7', 'opacity-80': 'opacity: 0.8', 'bg-opacity-50': '--tw-bg-opacity: 0.5'}
    for cls in [c for c in classes if c in op_map]:
        css_parts.append(f".{cls} {{ {op_map[cls]}; }}")

    # Overflow
    css_parts.append("\n/* ===== Overflow ===== */")
    ov_map = {'overflow-auto': 'overflow: auto', 'overflow-hidden': 'overflow: hidden', 'overflow-x-auto': 'overflow-x: auto', 'overflow-y-auto': 'overflow-y: auto'}
    for cls in [c for c in classes if c in ov_map]:
        css_parts.append(f".{cls} {{ {ov_map[cls]}; }}")

    # Transitions & Transforms
    css_parts.append("\n/* ===== Transitions & Animation ===== */")
    trans_map = {
        'transition': 'transition-property: color, background-color, border-color, fill, stroke, opacity, box-shadow, transform, filter, -webkit-backdrop-filter; transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, -webkit-backdrop-filter; transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, -webkit-backdrop-filter, -webkit-text-decoration-color; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms',
        'transition-all': 'transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms',
        'transition-colors': 'transition-property: color, background-color, border-color, fill, stroke, -webkit-text-decoration-color; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms',
        'transition-transform': 'transition-property: transform; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms',
        'transition-shadow': 'transition-property: box-shadow; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms',
        'transform': 'transform: translateX(var(--tw-translate-x, 0)) translateY(var(--tw-translate-y, 0)) rotate(var(--tw-rotate, 0)) skewX(var(--tw-skew-x, 0)) skewY(var(--tw-skew-y, 0)) scaleX(var(--tw-scale-x, 1)) scaleY(var(--tw-scale-y, 1))',
        'animate-slide-in': 'animation: slideIn 0.3s ease-out',
        'backdrop-blur': 'backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px)',
    }
    for cls in [c for c in classes if c in trans_map]:
        css_parts.append(f".{cls} {{ {trans_map[cls]}; }}")

    # Translate
    trans_x = {'translate-x-1/3': 'transform: translateX(33.333333%);', '-translate-x-1/3': 'transform: translateX(-33.333333%);', 'translate-x-1/4': 'transform: translateX(25%);', '-translate-x-1/4': 'transform: translateX(-25%);', 'translate-x-6': 'transform: translateX(24px);', 'translate-y-1/2': 'transform: translateY(50%);', '-translate-y-1/2': 'transform: translateY(-50%);'}
    for cls in [c for c in classes if c in trans_x]:
        css_parts.append(f".{cls} {{ {trans_x[cls]}; }}")

    # Cursor
    cursor_map = {'cursor-pointer': 'cursor: pointer', 'cursor-move': 'cursor: move', 'cursor-not-allowed': 'cursor: not-allowed'}
    for cls in [c for c in classes if c in cursor_map]:
        css_parts.append(f".{cls} {{ {cursor_map[cls]}; }}")

    # Object fit
    obj_fit = {'object-contain': 'object-fit: contain'}
    for cls in [c for c in classes if c in obj_fit]:
        css_parts.append(f".{cls} {{ {obj_fit[cls]}; }}")

    # Outline
    outline_map = {'outline-none': 'outline: 2px solid transparent; outline-offset: 2px'}
    for cls in [c for c in classes if c in outline_map]:
        css_parts.append(f".{cls} {{ {outline_map[cls]}; }}")

    # Resize
    resize_map = {'resize-none': 'resize: none'}
    for cls in [c for c in classes if c in resize_map]:
        css_parts.append(f".{cls} {{ {resize_map[cls]}; }}")

    # Z-index
    z_map = {'z-10': 'z-index: 10', 'z-50': 'z-index: 50', 'z-[60]': 'z-index: 60', '-z-10': 'z-index: -10'}
    for cls in [c for c in classes if c in z_map]:
        css_parts.append(f".{cls} {{ {z_map[cls]}; }}")

    # SR Only
    sr_only = '.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border-width: 0; }'
    if 'sr-only' in classes:
        css_parts.append(sr_only)

    # Filter
    filter_map = {'filter': 'filter: var(--tw-blur,) var(--tw-brightness,) var(--tw-contrast,) var(--tw-grayscale,) var(--tw-hue-rotate,) var(--tw-invert,) var(--tw-saturate,) var(--tw-sepia,) var(--tw-drop-shadow,)'}
    for cls in [c for c in classes if c in filter_map]:
        css_parts.append(f".{cls} {{ {filter_map[cls]}; }}")

    # Keyframes animation
    css_parts.append("""
/* ===== Custom Animations ===== */
@keyframes slideIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
""")

    return '\n'.join(css_parts)


css_content = generate_css(clean_classes)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(css_content)

size_kb = len(css_content.encode('utf-8')) / 1024
print(f"\n✅ Generated: {OUTPUT_FILE}")
print(f"   Size: {size_kb:.1f} KB (vs original 2865 KB)")
print(f"   Reduction: {(1 - size_kb/2865)*100:.1f}%")
print(f"   Classes covered: {len(clean_classes)}")
