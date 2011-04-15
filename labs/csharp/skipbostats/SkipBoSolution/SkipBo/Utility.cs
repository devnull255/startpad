using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

namespace SkipBo
{
    static public class Utility
    {
        // Create a reproducible sequence of random numbers
        static Random _random = new Random(0);
        public static Random Random()
        {
            return _random;
        }

        public static void Invariant(bool isAlwaysTrue, string failureMessage)
        {
            if (!isAlwaysTrue)
            {
                failureMessage = string.Format(string.Format("Invariant failed: {0}\n{1}", failureMessage, Environment.StackTrace));
                Logger.Write(failureMessage);
                throw new ApplicationException(failureMessage);
            }
        }
    }
}
