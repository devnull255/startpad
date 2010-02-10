using System;
using System.Collections.Generic;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using SkipBo;

namespace TestSkipBo
{
    class Histogram
    {
        int[] _histogram = new int[13];

        public void AddPile(Pile pile)
        {
            foreach (Card card in pile)
            {
                _histogram[card.Value]++;
            }
        }

        public void AssertFullDeck()
        {
            Assert.AreEqual(Board.SkipBos, _histogram[0], "Wrong number of skipbos");
            for (int index = 1; index < 13; index++)
            {
                Assert.AreEqual(Board.CardsPerValue, _histogram[index], "A suit has the wrong number of cards");
            }
        }
    }
}
