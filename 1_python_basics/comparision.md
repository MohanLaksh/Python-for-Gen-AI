| Feature / Property       | **List**                 | **Tuple**             | **Set**                | **Dictionary**              |
| ------------------------ | ------------------------ | --------------------- | ---------------------- | --------------------------- |
| **Syntax**               | `[ ]`                    | `( )`                 | `{ }`                  | `{ key: value }`            |
| **Ordered**              | ✅ Yes                    | ✅ Yes                 | ❌ No                   | ✅ Yes (Python 3.7+)         |
| **Mutable (changeable)** | ✅ Yes                    | ❌ No                  | ✅ Yes                  | ✅ Yes                       |
| **Allows Duplicates**    | ✅ Yes                    | ✅ Yes                 | ❌ No                   | ❌ Keys: No<br>✅ Values: Yes |
| **Index-based Access**   | ✅ Yes                    | ✅ Yes                 | ❌ No                   | ❌ (key-based)               |
| **Key–Value Pair**       | ❌ No                     | ❌ No                  | ❌ No                   | ✅ Yes                       |
| **Use Case**             | Ordered, changeable data | Fixed, read-only data | Unique items           | Fast lookup using keys      |
| **Performance**          | Moderate                 | Faster than list      | Very fast (membership) | Very fast (key access)      |
| **Can be Nested**        | ✅ Yes                    | ✅ Yes                 | ❌ No (mutable items)   | ✅ Yes                       |
| **Example**              | `[1, 2, 2, 3]`           | `(1, 2, 2, 3)`        | `{1, 2, 3}`            | `{"a": 1, "b": 2}`          |
