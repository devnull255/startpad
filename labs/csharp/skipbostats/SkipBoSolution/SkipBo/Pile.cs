using System;
using System.Collections.Generic;
using System.Text;

namespace SkipBo
{
    public class Pile : List<Card>
    {
        // Keep track of the number of piles allocated for each piletype
        private static Dictionary<PileType, int> _countOfPileTypes = new Dictionary<PileType, int>();
        private PileType _pileType;
        private readonly int _pileIndex;
        public int PileIndex
        {
            get { return _pileIndex; }
        }

        // Static initializer
        static Pile()
        {
            foreach (PileType pileType in Enum.GetValues(typeof(PileType)))
            {
                _countOfPileTypes[pileType] = 0;
            }
        }

        public Pile(PileType pileType)
        {
            _pileType = pileType;
            _pileIndex = _countOfPileTypes[pileType];
            _countOfPileTypes[pileType]++;
        }

        public PileType PileType
        {
            get { return _pileType; }
        }

        public Card Top
        {
            get
            {
                if (Count < 1)
                {
                    throw new InvalidPlayException("Tried to get Top of empty pile");
                }
                return this[Count-1];
            }
        }

        public bool HasCards
        {
            get { return this.Count > 0; }
        }

        public Card Pop()
        {
            Card card = Top;
            this.RemoveAt(this.Count - 1);
            return card;
        }

        public override string ToString()
        {
            return string.Format("{0}[{1}]", Enum.GetName(typeof(PileType), _pileType), _pileIndex);
        }
        // void Shuffle()
        // void AppendPile(pile)

        public bool IsLegalPlay(Card card, Pile pile, out int playedValue)
        {
            switch (_pileType)
            {
                case PileType.Reserve:
                case PileType.Discard:
                case PileType.Draw:
                case PileType.Hand:
                default:
                    playedValue = -1;
                    return false;

                case PileType.Build:
                    if (card.IsSkipBo)
                    {
                        if (!pile.HasCards)
                        {
                            playedValue = 1;
                        }
                        else
                        {
                            playedValue = pile.Top.PlayedValue + 1;
                        }
                        return true;
                    }

                    int requiredValue;
                    if (pile.Count == 0)
                    {
                        requiredValue = 1;
                    }
                    else
                    {
                        requiredValue = pile.Top.PlayedValue + 1;
                    }
                    if (card.Value == requiredValue)
                    {
                        playedValue = requiredValue;
                        return true;
                    }

                    playedValue = -1;
                    return false;
            }
        }

        public string ToString(string s)
        {
            StringBuilder stringBuilder = new StringBuilder();
            stringBuilder.AppendFormat("{0}[{1}]:", _pileType, _pileIndex);
            foreach (Card card in this)
            {
                stringBuilder.AppendFormat("{0},", card);
            }
            // Remove final ","
            if (this.Count > 0)
            {
                stringBuilder.Remove(stringBuilder.Length - 1, 1);
            }
            return stringBuilder.ToString();
        }
    }
}
