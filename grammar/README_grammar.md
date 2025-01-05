# **Draw++ Language Documentation**

## **Basics**
Each statement must end with a `;`.

### **Data Types**
Draw++ supports the following data types:
- `int` (64-bit integer)
- `float` (64-bit float)
- `bool` (boolean)
- `color` (for color values)

### **Variables**
- **Variables:** `var <type> <identifier> = <expression>;`
  - Example: `var int length = 10;`

### **Control Flow**
**Conditions :**
- `if (<condition>) { <statement_list> } elif (<condition>) { <statement_list> } else { <statement_list> }`

**Loops:**
- `while (<condition>) { <statement_list> }`
- `for (<initialization>; <condition>; <update>) { <statement_list> }`

### **Comments**
- Single-line: `// This is a comment`
- Multi-line: `/* This is a multi-line comment */`

### **Operators**
- **Arithmetic:** `+`, `-`, `*`, `/`, `%`
- **Compound:** `+=`, `-=`, `*=`, `/=`
- **Relational:** `<`, `<=`, `>`, `>=`, `==`, `!=`

---

## **Keywords**
Explaining here special keyword `cursor`.

### **Cursor**
The cursor is the central object used for drawing. It is a special variable type.
- **Declaration :** `<cursor_creation> ::= cursor <identifier> = create_cursor (<expression>, <expression>)`
    - Example : `cursor variable = create_cursor(startX, startY);`

It has the following properties :
**Position and Movement:**
- `.position(x, y)` sets the cursor position.
- `.move(distance)` moves the cursor forward in its current orientation.
- `.rotate(angle)` rotates the cursor.

**Style:**
- `.color(<color_value>)` sets the drawing color.
- `.thickness(value)` sets the line thickness.

**Visibility:**
- `.visible()` shows the cursor at the requested moment.

Examples : `variable.position(100, 200);`, `variable.color(RED);`, `variable.thickness(5);`, `variable.move(50);`

### **Drawing shapes**
Shapes are drawn using methods of the cursor variable:
- **Line:** `.draw_line(length)`
- **Rectangle:** `.draw_rectangle(width, height, filled)`
- **Circle:** `.draw_circle(radius, filled)`
- **Triangle:** `.draw_triangle(base, height, filled)`
- **Ellipse:** `.draw_ellipse(width, height, filled)`

    - Examples : `variable.draw_rectangle(100, 50, true);`, `variable.draw_circle(30, false);`

### **Color Values**
- Predefined colors: `RED`, `GREEN`, `BLUE`, etc. Find a full list in [this file](https://github.com/guinat/cytech-project-drawpp-ing1-20242025/blob/main/grammar/drawpp_grammar.bnf).
- Custom colors: `rgb(r, g, b)` where `r`, `g`, `b` are integers between 0-255.