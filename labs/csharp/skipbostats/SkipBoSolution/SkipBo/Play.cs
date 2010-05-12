using System;

namespace SkipBo
{
    // Discription of a skipbo play (one card)
    public enum PileType {Reserve, Hand, Discard, Build, Draw};

    public class InvalidPlayException : ApplicationException
    {
        private string _message;

        public InvalidPlayException(string message)
        {
            _message = "Invalid Play: " + message;
        }
        public InvalidPlayException(Play play)
        {
            _message = GenerateErrorMessage(play);

        }

        public override string Message
        {
            get { return _message; }
        }

        private static string GenerateErrorMessage(Play play)
        {
            return "Invalid Play: " + play;
        }
    }

    public class Play
    {
        private readonly int _fromPileCardIndex;
        public int FromCardIndex
        {
            get { return _fromPileCardIndex; }
        }

        private readonly Pile _fromPile;
        public Pile FromPile
        {
            get { return _fromPile; }
        }
        private readonly Pile _toPile;
        private Card _fromCard;

        public Pile ToPile
        {
            get { return _toPile;  }
        }

        public PileType ToPileType
        {
            get { return _toPile.PileType; }
        }

        public Card PlayedCard
        {
            get { return _fromCard; }
        }


        public Play(Pile fromPile, Pile toPile): this(fromPile, fromPile.Top, toPile)
        {
            
        }
        public Play(Pile fromPile, Card fromCard, Pile toPile)
        {
            _fromPile = fromPile;
            _fromPileCardIndex = fromPile.IndexOf(fromCard);
            _fromCard = fromCard;
            _toPile = toPile;
            Logger.Write(GenerateToString());
        }

        private string GenerateToString()
        {
            return string.Format("{0}[{1},{2}]({3}) -> {4}[{5},{6}]({7})", Enum.GetName(typeof(PileType), _fromPile.PileType), _fromPile.PileIndex, _fromPile.IndexOf(_fromCard), _fromCard, _toPile.PileType, _toPile.PileIndex, _toPile.Count, _toPile.Count==0? "empty": _toPile[_toPile.Count-1].ToString());
        }

        public override string ToString()
        {
            return GenerateToString();
        }

        public bool IsValid()
        {
            PileType fromPileType = _fromPile.PileType;
            PileType toPileType = _toPile.PileType;

            if (_fromPile.Count <= 0)
            {
                return false;
            }

            switch (fromPileType)
            {
                case PileType.Build:
                    // Can never play from a build pile
                    return false;
                case PileType.Discard:
                    // Can only play from discard to build pile
                    if (toPileType != PileType.Build)
                        return false;
                    return true;
                case PileType.Hand:
                    // Can only play from hand to build or discard pile
                    if (toPileType != PileType.Build && toPileType != PileType.Discard)
                        return false;
                    return true;
                case PileType.Reserve:
                    // Can only play from reserve to build
                    if (toPileType != PileType.Build)
                        return false;
                    if (_fromPileCardIndex < 0)
                        return false;
                    return true;
                case PileType.Draw:
                    // Can only "play" (deal) from draw pile to players hand
                    if (_toPile.PileType != PileType.Hand)
                        return false;
                    return true;
                default:
                    throw new InvalidPlayException(this);
            }
        }
    }
}
