using System;
using System.Collections.Generic;
using System.Text;

namespace SkipBo
{
    public class InvalidCardException : ApplicationException
    {
        
    }

    public class Card
    {
        public static readonly int SkipBoValue = 0;

        private int _value;
        private bool _isSkipBo;
        private int _playedValue;


        // This private parameterless constructor is required
        private Card()
        {
            
        }

        public Card(int value)
        {
            if (!(value == SkipBoValue || (value >= 1 && value <= 12)))
            {
                throw new InvalidCardException();
            }

            if (value == SkipBoValue)
            {
                _isSkipBo = true;
            }
            this._value = value;
        }

        public override string ToString()
        {
            if (_isSkipBo)
            {
                return "SB";
            }
            else
            {
                return _value.ToString();
            }
        }
        // bool IsSkipBo
        // Nullable<int> Value (1-12) or null

        public int Value
        {
            get { return _value; }
        }

        public bool IsSkipBo
        {
            get { return _isSkipBo; }
        }

        public int PlayedValue
        {
            get { return _isSkipBo? _playedValue: _value; }
            set { _playedValue = value; }
        }
    }
}
