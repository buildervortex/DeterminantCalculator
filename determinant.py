import copy


class MatrixDeterminantCalculator:
    def multiplyRow(self, row: list[float], scaler: float) -> list[float]:
        scaledRow = []
        for number in row:
            scaledRow.append(number*scaler)
        return scaledRow

    def substractRow(self, row1: list[float], row2: list[float]) -> list[float]:
        subRow = []
        for index in range(0, len(row2)):
            subRow.append(row1[index] - row2[index])
        return subRow

    def isSquareMatrix(self, matrix: list[list[float]]) -> bool:
        rowCount = len(matrix)

        for row in matrix:
            if len(row) != rowCount:
                return False

        return True

    def swapToMakeNonZeroPivotPoints(self, matrix: list[list[float]]) -> tuple[int, list[list[float]]]:

        matrixCopy = copy.deepcopy(matrix)
        matrixSize = len(matrixCopy)

        sign = 1

        # Loop until row before the last row in the matrix
        for rowIndex in range(0, (matrixSize - 1)):

            # Set the pivot point index
            pivotIndex = rowIndex

            # If the matrix pivot point is not zero, then continue to the next row
            if matrixCopy[rowIndex][pivotIndex] != 0:
                continue

            # go through the bottom rows and checks a row that has a non zero element for the pivot point
            for downRowIndex in range(rowIndex+1, matrixSize):

                # skip the downrow and go to next down row if current down row contains zero at the pivot point
                if matrixCopy[downRowIndex][pivotIndex] == 0:
                    continue

                # swap the rows because the down row contains non zero element at the pivot point
                matrixCopy[rowIndex], matrixCopy[downRowIndex] = matrixCopy[downRowIndex], matrixCopy[rowIndex]

                # change the sign to keep the track of the swapping
                sign *= -1

                # break the down row selection because the swapping already done
                break

        return sign, matrixCopy

    # perform the guassian elimination to create the U ( upper triangle matrix )
    def guassianElimination(self, matrix: list[list[float]]):

        # get copy of the given matrix
        matrixCopy = copy.deepcopy(matrix)

        matrixSize = len(matrixCopy)

        for pivotRowIndex in range(0, (matrixSize - 1)):

            # get the main current row pivot point index
            pivotColumnIndex = pivotRowIndex

            # Skip processing the current row if the pivot point is zero, because it cause zero division error
            if matrixCopy[pivotRowIndex][pivotColumnIndex] == 0:
                continue

            # Loop through the down rows. multiply each row by a scaler for the current row to make the down row pivot point 0
            for downRowIndex in range(pivotRowIndex + 1, len(matrixCopy)):

                # If the pivot point already zero, continue to the next down row
                if matrixCopy[downRowIndex][pivotColumnIndex] == 0:
                    continue

                # get the mulplier which makes the down row pivot index 0
                multiplier = matrixCopy[downRowIndex][pivotColumnIndex] / \
                    matrixCopy[pivotRowIndex][pivotColumnIndex]

                # get the substractor by multipling the current row with multiplier
                substractor = self.multiplyRow(
                    matrixCopy[pivotRowIndex], multiplier)

                # substract the substractor from down row to make the pivot point zero
                matrixCopy[downRowIndex] = self.substractRow(
                    matrixCopy[downRowIndex], substractor)

        return matrixCopy

    # calculate the determinant of a upper triangle matrix by multiplying all the values in the diagonal
    def determinantOfUpperTriangleMatrix(self, matrix: list[list[float]], sign: int):
        # If sign is 0, return 0 immediately
        if sign == 0:
            return 0

        pivotPoints = []
        determinant = 1

        # loop through the matrix and save all the diagonal numbers in the pivotPoints list
        for rowIndex in range(0, len(matrix)):
            pivotPoints.append(matrix[rowIndex][rowIndex])

        # calculate the multiplier of diagonal line numbers
        for point in pivotPoints:
            determinant *= point

        # multiply the determinant by the sign
        return determinant * sign

    # combine all the above methods to create single point of use
    def calculateMatrixDeterminant(self, matrix: list[list[float]]) -> float:

        if not self.isSquareMatrix(matrix=matrix):
            raise ValueError("Matrix is not a square matrix")

        sign, sortMatrix = self.swapToMakeNonZeroPivotPoints(matrix)

        # If sign is 0, determinant is 0
        if sign == 0:
            return 0

        upperTriangleMatrix = self.guassianElimination(sortMatrix)

        result = self.determinantOfUpperTriangleMatrix(
            upperTriangleMatrix, sign)

        # Round to handle floating point errors, but don't use ceil
        if abs(result - round(result)) < 1e-10:
            return round(result)
        return result
