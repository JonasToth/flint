  subroutine locate(l,n,array,var,pos)
    !> Search the index of given value in sorted 1D array of unique values.
    !>
    !> It uses a binary search algorithm.
    implicit none
    integer(int_p), intent(in) :: l !> Initial guess of lower limit.
    integer(int_p), intent(in) :: n !> Size of array.
    real(real_p), dimension(n), intent(in) :: array !> Sorted array to search.
    real(real_p), intent(in) :: var !> Value to find.
    integer(int_p), intent(out) :: pos !> Resulting index.

    ! interrupting comment

    integer(int_p) :: jl !> Lower limit.
    integer(int_p) :: jm !> Midpoint
    integer(int_p) :: ju !> Upper limit
    ! Initialize lower limit (L=0 FOR A NORMAL VECTOR!).
    jl=l
    ! Initialize upper limit.
    ju=jl+n+1
    ! If we are not yet done compute a midpoint.
    pos=max(l+1,pos)
    return
  end subroutine locate


  pure function equal(arg1,arg2) result(res)
      !> Returns whether the arguments are equal to machine precision
      real(real_p), intent(in) :: arg1, arg2
      logical :: res
      res = (abs(arg1-arg2) < REALTOL)
  end function equal

  subroutine print_assertion_error(filename, line, error_msg)
    implicit none

    character(len=*), intent(in) :: filename
    integer(int_p), intent(in)   :: line
    character(len=*), intent(in) :: error_msg
    character(len=10)            :: line_string

    write (line_string, '(I2)') line
    write (*,*) trim(filename) // ": " // trim(line_string) // ": " // trim(error_msg)
  end subroutine print_assertion_error
