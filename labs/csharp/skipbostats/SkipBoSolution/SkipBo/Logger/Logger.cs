using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

namespace SkipBo
{
    public static class Logger
    {
        public static bool IsWriting = true;

        public static void Write(string message)
        {
            if (IsWriting)
            {
                Debug.WriteLine(message);
            }
        }
    }
}
