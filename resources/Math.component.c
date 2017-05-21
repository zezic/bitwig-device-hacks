component math2000
{
   audio_inport f32 a;
   audio_inport f32 b;
   value_inport i32 op;
   audio_outport f32 out;
   f32 prev_value = 0;
   f32 rate;

   process
   {
      // 0 MUL:DIV
      // 1 ADD:SIG
      // 2 SUB:POW
      // 3 MIN:LOG
      // 4 MAX:SIN
      // 5 QUA:EMA

      if (op == 0) {
         out = a / (b * 10);
      }
      else if (op == 1) {
         out = copysign(1.0, a + b);
      }
      else if (op == 2) {
         out = pow(a, b * 10);
      }
      else if (op == 3) {
         out = log(a + b);
      }
      else if (op == 4) {
         out = sin(a * b * 20 * 3.14159265);
      }
      else if (op == 5) {
         rate = 0.0001 * fabs(b);
         out = a * rate + prev_value * (1-rate);
         prev_value = out;
      }
   }
}
