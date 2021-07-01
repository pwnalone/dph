# Diffie-(Pohlig)-Hellman (DPH)

### Description

[1]: https://www.nccgroup.com/globalassets/our-research/uk/whitepapers/2016/06/how-to-backdoor-diffie-hellman.pdf

**DPH** is a utility to create and exploit Nobody-But-Us (NOBUS) backdoors in the Diffie-Hellman
(DH) protocol. It works by generating DH parameters, which are specially crafted to produce
indistinguishable encryptions against anyone without intricate knowledge as to how the parameters
were chosen. For an in-depth explanation on how this works, read this [white paper][1] from 2016 by
NCC Group.
